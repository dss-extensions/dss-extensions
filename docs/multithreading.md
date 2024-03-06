---
html_theme.sidebar_secondary.remove: true
---

# Multiple engines and multithreading

*DSS-Extensions: Multiple DSS engines and multithreading aspects*

Since AltDSS/DSS C-API v0.12 (July 2022), many of the projects under DSS-Extensions allow users to run custom multithreaded code. This is enabled by a different implementation of the DSS engine in AltDSS/DSS C-API compared to the official OpenDSS distribution. This document tries to highlight some of the aspects that are different.

Overall, the adopted architecture allows more usage scenarios beyond the original actor approach from OpenDSS v8+, and has a tested, multi-platform implementation.


## History

For a few years, OpenDSS was distributed/developed in two branches:

- **Version 7.x**: The original version, without explicit parallel-machine support.
- **Version 8.x+**: Introduces a parallel-machine (**PM**) architecture, based on actors.

When our base project AltDSS/DSS C-API was first published, it supported on Version 7.x, which was the main stable branch at the time.

Soon after the first release of DSS C-API, [initial support for the PM version was added](https://sourceforge.net/p/electricdss/discussion/861976/thread/525c13df/#b043), including Python integration.

Just like the two versions were maintained in the official OpenDSS, DSS C-API followed with two different binaries for a few years.

The main OpenDSS followed with v8+, dropping releases for the v7 codebase by version 9.0, released on June 2020. In AltDSS/DSS C-API, another alternative was investigated, published later as the main branch in July 2022. In the meantime, support for the code derived from the official PM variation was dropped to simplify maintenance.

## Architecture of OpenDSS v7 vs. v8+

Both OpenDSS variations is based on a classic paradigm of using global variables to track state. There are two main aspects that differ between these two variants.

The first aspect can be seen in `DSSGlobals.pas`. Version 8+ uses arrays for each class instance or value that used to be a single item. Some snippets for comparison:

::::{grid} 2
:::{grid-item-card} [OpenDSS Version 7](https://sourceforge.net/p/electricdss/code/3723/tree/trunk/Version7/Source/Common/DSSGlobals.pas)
```pascal
ActiveCircuit   :TDSSCircuit;
ActiveDSSClass  :TDSSClass;
LastClassReferenced:Integer;  // index of class of last thing edited
ActiveDSSObject :TDSSObject;
// ...
// Some commonly used classes   so we can find them easily
LoadShapeClass     :TLoadShape;
TShapeClass        :TTshape;
PriceShapeClass    :TPriceShape;
XYCurveClass       :TXYCurve;
GrowthShapeClass   :TGrowthShape;
SpectrumClass      :TSpectrum;
```
:::

:::{grid-item-card} [OpenDSS Version 8+](https://sourceforge.net/p/electricdss/code/3723/tree/trunk/Version8/Source/Common/DSSGlobals.pas)
```pascal
ActiveCircuit   :Array of TDSSCircuit;
ActiveDSSClass  :Array of TDSSClass;
LastClassReferenced:Array of Integer;  // index of class of last thing edited
ActiveDSSObject :Array of TDSSObject;
// ...
// Some commonly used classes   so we can find them easily
LoadShapeClass     :Array of TLoadShape;
TShapeClass        :Array of TTshape;
PriceShapeClass    :Array of TPriceShape;
XYCurveClass       :Array of TXYCurve;
GrowthShapeClass   :Array of TGrowthShape;
SpectrumClass      :Array of TSpectrum;
```
:::
::::

The second aspect is how the arrays are used. The codebase for version 7 is simpler since it just refers to the global values directly. Version 8+ needs some way to know which item in the array it should use. There are two main ways this happens. The first one is the introduction of the `ActorID` function argument in a lot of places. For example, here's the `TVsourceObj` class:

::::{grid} 2
:::{grid-item-card} [OpenDSS Version 7](https://sourceforge.net/p/electricdss/code/3723/tree/trunk/Version7/Source/PCElements/VSource.pas)
```pascal
Procedure RecalcElementData; Override;
Procedure CalcYPrim; Override;

Function  InjCurrents:Integer; Override;
Procedure GetInjCurrents(Curr:pComplexArray); Override;
Procedure GetCurrents(Curr: pComplexArray);Override;
```
:::

:::{grid-item-card} [OpenDSS Version 8+](https://sourceforge.net/p/electricdss/code/3723/tree/trunk/Version8/Source/PCElements/VSource.pas)
```pascal
Procedure RecalcElementData(ActorID : Integer); Override;
Procedure CalcYPrim(ActorID : Integer); Override;

Function  InjCurrents(ActorID : Integer):Integer; Override;
Procedure GetInjCurrents(Curr:pComplexArray; ActorID : Integer); Override;
Procedure GetCurrents(Curr: pComplexArray; ActorID : Integer);Override;
```
:::
::::

The second way that the array index is selected is via the `ActiveActor` global variable. Still in `VSource.pas`:

::::{grid} 2
:::{grid-item-card} [OpenDSS Version 7](https://sourceforge.net/p/electricdss/code/3723/tree/trunk/Version7/Source/PCElements/VSource.pas)
```pascal
Function TVsource.NewObject(const ObjName:String):Integer;
Begin
    // Make a new voltage source and add it to Vsource class list
    With ActiveCircuit Do
    Begin
      ActiveCktElement := TVsourceObj.Create(Self, ObjName);
      Result := AddObjectToList(ActiveDSSObject);
    End;
End;
```
:::

:::{grid-item-card} [OpenDSS Version 8+](https://sourceforge.net/p/electricdss/code/3723/tree/trunk/Version8/Source/PCElements/VSource.pas)
```pascal
Function TVsource.NewObject(const ObjName:String):Integer;
Begin
    // Make a new voltage source and add it to Vsource class list
    With ActiveCircuit[ActiveActor] Do
    Begin
      ActiveCktElement := TVsourceObj.Create(Self, ObjName);
      Result := AddObjectToList(ActiveDSSObject[ActiveActor]);
    End;
End;
```
:::
::::

This global `ActiveActor` is mostly what limits what the engine can do, since it can only have one actor active at one, in the current implementation. As a consequence, some operations must not be run in parallel.

The global structures being arrays and requiring the index to be used for each of them can lead to some repetition in the code. For example, an excerpt from [`Solution.pas`](https://sourceforge.net/p/electricdss/code/3723/tree/trunk/Version8/Source/Common/Solution.pas#l1640):

```pascal
    DevClassIndex := ClassNames[ActorID].Find('reactor');
    LastClassReferenced[ActorID] := DevClassIndex;
    ActiveDSSClass[ActorID] := DSSClassList[ActorID].Get(LastClassReferenced[ActorID]);
    elem        := ActiveDSSClass[ActorID].First;
```

### Parallel-machine implementation

In v8+, the [actor model](https://en.wikipedia.org/wiki/Actor_model) is used to allow multithreaded code. As seen in the previous code snippets, the global array indices represent an actor index `ActorID` or `ActiveActor`. Each actor thread (`TSolver`) is created with a matching `ActorID`. The thread starts loop waiting commands to run for the circuit associated with this `ActorID`. The commands are mostly solution algorithms, some solution state manipulation, or thread termination.

Past versions used to set the priority of the process to realtime, while also setting thread priorities high. Current versions, as of February 2024, do not set the process priority anymore.

## Architecture of AltDSS/DSS C-API: DSSContext

It is important to note that the decision to follow another architecture on DSS-Extensions was based on multiple reasons. 

One of the main reasons was that maintaining and debugging multithreaded code with a different compiler (EPRI's OpenDSS uses Delphi, DSS-Extensions use Free Pascal), in multiple operating systems, is challenging. 

A second reason was that the DSS C-API codebase has been slowly refactored, with the end goal of porting/switching at once to another programming language (C++), so some aspects have been handled since 2018, little by little. It made sense to invest time into a more common approach when migrating older, single-threaded codebases to allow multithreading: introduce the encapsulation of the global variables into a dedicated context. This context is then propagated in most functions of the classic API.

What happened:

- The version 8+ code previously maintained in DSS C-API was dropped.
- The codebases from version 7 and version 8+ were carefully compared to find potential issues (a few were found and reported).
- Most of the global variables where encapsulated in a new `TDSSContext` class.
- Most classes now receive the DSS Context as the first parameter.
- A few helper functions, properties, and helper classes were created to minimize the code changes. For example, some classes expose a function `ActiveCircuit` that returns `DSSContext.ActiveCircuit`.
- A global variable `DSSPrime` was introduced to represent the default DSS Context, which is the DSS engine that is created by default when the library is loaded. This is required for backwards compatibility.
- The API code was updated to use `DSSPrime` anywhere the engine was used.
- Finally, a script automatically duplicates the API code, creating new versions that take the DSS Context as a pointer parameter. For example, `double Loads_Get_kW(void)` is derived into `double ctx_Loads_Get_kW(const void* ctx)`. Both the C headers and the Pascal code is handled.

Couple of side notes:

- Although not significant, it was noticed that the DSSContext implementation was slightly faster than the previous version due to memory locality differences.
- AltDSS/DSS C-API is also slowly moving away from concepts like `ActiveCircuit`; instead, the circuit is either passed explicitly or directly associated. This is a work-in-progress migration that should clean the code a bit more.

### Parallel-machine implementation

The PM implementation follows the general concepts of the official OpenDSS implementation, using the actor model. The main difference is that instead of relying on an `ActorID` integer index, the actor thread (also `TSolver` in DSS C-API) gets a `TDSSContext` instance. There are a couple of locks to avoid issues noticed when running on platforms besides Windows.

While the official implementation sets thread priority, it is not set on DSS C-API.

Overall, this implementation is quite compatible with the official version, exposing the same API to the user.

## Linux-specific notes

To achieve safe multithreading on Linux and macOS, there were a lot of small tweaks, and a big one: the memory allocator is now the system (C) allocator, instead of the default Free Pascal internal allocator.

Unfortunately, the default allocator on many Linux distributions does not work great for OpenDSS workloads.

To achieve better performance in general, both for single- and multithreading, we recommend ensuring that a good allocator is used. We have tested a bunch of allocators and recommend the following two:

- [jemalloc](http://jemalloc.net/)
- [mimalloc](https://github.com/microsoft/mimalloc)

Other allocators (e.g [tcmalloc](https://google.github.io/tcmalloc/)) also have good performance, but these two dominated the benchmarks. In doubt, be sure to test for your use-case, ideally with a real-life scenario.

We recommend reading a little about those before using them, but you can use `LD_PRELOAD` to apply the allocator to the whole program. For example, if you'd like to run a Python script, appending the command with the target allocator library is enough:

```shell
LD_PRELOAD=/usr/lib64/libmimalloc.so python my_script.py
```

You can also use allocator-specific options — check the documentation to see what's available. For example, when using jemalloc, it's also good to use background threads:

```
MALLOC_CONF=background_thread:true LD_PRELOAD=/usr/lib64/libjemalloc.so python my_script.py
```

Note that the path `/usr/lib64` varies according to the Linux distribution. Some may use just `/usr/lib`. Both jemalloc and mimalloc are also available in conda-forge, for example, so users do not require administrator/root permissions to use them.

Effectively, using these allocators brings a lot more performance for DSS C-API 0.12+ than DSS C-API 0.10 or earlier with the internal allocator, even on single-threaded processes.
