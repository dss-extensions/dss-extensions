# DSS-Extensions — OpenDSS: Intro to the classic API

https://github.com/dss-extensions/dss-extensions/issues/12
https://github.com/dss-extensions/OpenDSSDirect.jl/issues/87



This document is an introduction to the concepts of the classic OpenDSS API as presented by the official COM interface, the official OpenDSSDirect.DLL, and all the DSS-Extensions (except classes, properties and functions marked as API extensions), that is: DSS-Python, OpenDSSDirect.py, OpenDSSDirect.jl, DSS Sharp, DSS MATLAB, and the classic namespace of `dss.hpp`.

We propose an alternative API in....


## General layout

OpenDSS in general follows the concept of active objects throughout the API and even internally in many places. So, there are global variables that track the active object of each of the element classes, plus a few extras. As of our implementation of DSS C-API 0.13.1, the valid DSS classes are listed below:

-
-
-
-
-
-
-
-

The official OpenDSS has a few more such as `Generic5` and `FMonitor` (both of which we decided not to port yet), and a few other classes which are under development. 

As we can see from the list, only a fraction of the classes have equivalent APIs, and those are usually limited in certain aspects, not exposing all DSS data properties and so on. At the same time, there are certain functions and properties only available in an easily digestible format through the API.


## DSS properties


### Example: ...


## The Text interface

### Example: ...

### Caveats

- Performance
- Parsing
- etc.

## Class-specific APIS and "Active..."

To better illustrate this organization

### Example: transformers

- How to activate?

- How to access data?


### Example: loads


### Caveats

- Various functions, properties and OpenDSS commands can alter the active elements. This can be surprising and error-prone.
- The `Lines` API, specifically, does not track the active line object explicitly. Instead, the active circuit element is used, so it can also lead to some more surprises. For example, if you were using a line and then activate a load, you would need to reactivate the line before you can use it again even through the `Lines` API. This doesn't happen for all other elements. 

## What about buses?

You can access the buses from the dedicated API, but buses are not the same as other elements.

Buses in OpenDSS are defined implicitly when defining the circuit elements. After the basic circuit information is collected, you can complement it by passing information such as bus coordinates (`BusCoords` command, or the `x` and `y` properties from the API) and voltages (`SetkVBase` or `CalcVoltageBases` commands).

