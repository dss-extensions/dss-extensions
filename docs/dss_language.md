---
myst:
  html_meta:
    "description lang=en": |
      Description of the OpenDSS scripting language and data format for the DSS components, as seen in the implementation from DSS-Extensions (AltDSS/DSS C-API).
html_theme.sidebar_secondary.remove: true
---

# DSS Language

*OpenDSS Commands and Properties, DSS scripts.*

This section of the documentation contains some notes about the DSS scripting language and tables generated from the commands, options and properties for the DSS components at script level, as exposed in the DSS-Extensions version of the OpenDSS engine. One could consider this a complement to [EPRI's OpenDSS documentation](https://opendss.epri.com/opendss_documentation.html). The usual disclaimer that DSS-Extensions is not supported by EPRI applies, as well as the reminder that we try to keep the core of the engine very compatible.

A separate document will be developed in the future to detail **API** functions and general usage recommendations for the projects under DSS-Extensions. At the moment, there are various documentation pages linked on the main site and some subproject sites.

Since the extensive majority of properties and elements are compatible, this document can be useful when using either the official OpenDSS implementation or the DSS-Extensions version (DSS C-API engine), consumed through the several [DSS-Extensions projects](https://dss-extensions.org/projects) (in Python, Julia, MATLAB, C#, Go, Rust or C++), or through the COM API of the official OpenDSS. If you are using the official OpenDSS, when in doubt check the [official documentation](https://opendss.epri.com/opendss_documentation.html) and/or [source code](https://sourceforge.net/p/electricdss/code/HEAD/tree/).

As a final note, keep in mind that not all commands are implemented in the DSS-Extensions engine, and interactive commands like plots are missing (on purpose) or disabled by default. The Python packages can use the [work-in-progress plotting backend from DSS-Python](https://dss-extensions.org/DSS-Python/examples/Plotting) that can be enabled at runtime. For other use cases, we recommend using EPRI's OpenDSS distribution.

**Is this just a dump of the OpenDSS help?** ***No.*** This is generated from the internal schema, currently being consolidated in [AltDSS-Schema](https://github.com/dss-extensions/AltDSS-Schema) for JSON Schema, and it's the result of a lot of work done specifically on the internals of the AltDSS/DSS C-API library. The help/description text was also edited and adapted, which more changes planned to be integrated in the future.

Of special note, the [AltDSS](https://dss-extensions.org/AltDSS-Python/) package in Python has implementations for the enumerations listed here and can be used to complement both OpenDSSDirect.py and DSS-Python. Integration for further programming languages is planned as a future step.

:::{note}
The tables were complemented with a selection of units and default values, based on the work done for the AltDSS-Schema project. Some default values were hidden to avoid confusion, especially for "on array" values that are represented internally as arrays.
:::

## Brief notes

The DSS language supports various commands for manipulating the system, including creation of the circuit elements, powerflow solution, and exporting results (mostly in CSV and text files). In general, most of OpenDSS is case insensitive, including the commands. Beware though that when using DSS-Extensions on case-sensitive filesystems, the file names and paths will respect this aspect of the system.

Some commands have some special handling of the text parameters. The `new` and `edit` commands, though, mostly follow the same standard and are the most important part for creating new circuits from scratch. A typical `new` command would look like:

```
New Component.new_name a=10 b=20 d=30
```

From that:

- `Component` would be one of the DSS classes listed here. Some non-circuit classes allow creation before a circuit is created, but most require a circuit.
- `a`, `b`, and `d` are the names of the properties being edited.
- `10`, `20`, and `30` are the values being associated to the properties `a`, `b`, and `d`, respectively.

Assuming the index of each property is...

- `a`: 1
- `b`: 2
- `c`: 3
- `d`: 4

...one could omit the properties that follow the natural sequence, like below. This is not recommended in all scenarios though (read more bellow).

```
New Component.new_name 10 20 d=30
```

You can also use `~` (or `MORE`) command to continue editing in multiple lines:

```
New Component.new_name a=10 
~ b=20
~ d=30
```

One can also add comments with `!` or `//`, e.g. this would comment the whole statement:

```
! New Component.new_name a=10 b=20 d=30
```

And this would add a comment on a single line:

```
New Component.new_name a=10  
~ b=20 ! some comment about b
~ d=30 
```

For easier post-processing, if ever required, it is sometimes useful to prepend with some info, especially when converting from other circuit formats:

```
! new_name comes from DB xyz, original id 1234
New Component.new_name a=10 b=20 d=30
```

Since various properties have side-effects, the order the properties are provided is important. Notably, most sizing properties (like `phases`, `nphases`, `nconds`) allocate memory for the arrays of some elements.

For more, check the official OpenDSS documentation that comes with the software installation and https://opendss.epri.com/CircuitModelConcept.html — please note that note all examples follow the recommendations below. That is, please do not blindly follow every example without at least some critical thinking.

For scripts and other examples from the official OpenDSS, DSS-Extensions keeps a separate repo already prepared for multi-platform usage at https://github.com/dss-extensions/electricdss-tst

## Recommendations

These are mostly targeting users of large scale circuits, which typically are created using some kind of automation. Some are good to follow even on small scripts that need to endure changes in OpenDSS.

- **Always name each property.** For `.dss` files that need to be reused year later or with different OpenDSS versions in general. OpenDSS may introduce new properties in the middle of the list of properties, potentially breaking old scripts which don't include the names of the properties. Besides that, it's also good for humans to be able to quickly grasp the contents of the files without having to resort to the list of properties.
    - If, on the other hand, your scripts are generated on the fly and you can ensure the correct order to respect the index of the properties, there is no harm and it's probably incrementally faster.
- **Avoid short forms.** Like the lack of property names, this may also be affected by future changes in OpenDSS, introducing subtle issues that may be hard to spot. From the readability perspective, overusing short forms is also bad.
- **Use a consistent formatting standard.** Although most extra whitespace is ignored and OpenDSS allows multiple field and element separators, it's better to use a single standard.
- **Don't overuse `~` (`MORE`).** Each line starts and closes an edit cycle. When closing the edit cycle, OpenDSS may update some internal properties (internally `RecalcElementData`)
- **Avoid block comments.** Since there are very few good text-formatters with syntax highlighting for OpenDSS, block comments can be sometimes hard to spot.
- **Avoid inline RPN in large circuits.** For circuits exported from other sources, it is better to avoid using inline RPN math. For scripts written directly in OpenDSS, RPN math makes perfect sense to avoid manually calculating some values, but when exporting circuits or using APIs such as DSS-Extensions and the official COM API, it's better to precalculate the values in the hosting language (e.g. C#, Python, Julia, MATLAB, etc.), since most are more than capable of handling math.

## Conventions of this site

The property types are roughly defined in the table below.

| Property type | Description |
| :-- | :-- |
| boolean | Boolean values can be `yes`, `true`, `no`, `false`. Short forms allowed. |
| integer | Integer value. Many properties require positive values. |
| real | Real number, internally represent as floating-point numbers (almost all are `float64`). |
| string | General text; remember to enclose in quoting separators if it contains whitespace or other separators. |
| string (from enum.) | A string that must match the allowed enumerated values. Short forms are allowed (but discouraged). The allowed values are documented in a separated table. |
| string (bus def.) | A bus definition. It may be just the bus name, or more typically the bus followed by the nodes of the specific connection like `busxyz.1.2.4`. |
| complex | Complex number, passed an array of two real numbers, e.g. `1 + 2i` can be written as `[1, 2]` and other variations. |
| array of … | lists of the primary types above, like `[1,2,3]`, `[1 2 3]`, `(1, 2, 3)`, etc. For arrays of reals that represent matrices, check the description for some special behavior.|

Some items are marked:

- **deprecated**: either have been removed or can still be used but are discouraged due to known limitations. Notably, the `like` property doesn't copy all properties for some classes, and some properties were removed in the transition from OpenDSS 8.x to 9.0.
- **action**: may manipulate the data from the object being edited. Some are not typically used as data input, but are used during simulations to manipulate state.
- **redundant**: OpenDSS has multiple ways of defining the same data. Some properties are trivially derived from others. For example, `Generator` exposes both `MVA` and `kVA`, which change just the unit in which the rating of the generator is provided.
- **on array**: Items are marked "on array" to quickly remind the user that the value references an array value, indexed by another property, notably in `LineGeometry` (`cond`) and `Transformer` (`wdg`).

(circuit-elements)=
### Circuit Elements

Circuit elements ("CktElements") are objects associated to the circuit, i.e. any non-general object:

- [PD Elements](#pd-elements)
- [PC Elements](#pc-elements)
- [Meter Elements](#meter-elements)
- [Control Elements](#control-elements)

## DSS Reference

```{toctree}
:maxdepth: 2
dss-format/Enumerations
dss-format/Commands
dss-format/Options
dss-format/toc_general
dss-format/toc_me
dss-format/toc_control
dss-format/toc_pde
dss-format/toc_pce
```
