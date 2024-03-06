---
sd_hide_title: true
---
# Documentation

Be sure to check the [FAQ](#faq). It addresses some common issues.

The quality and volume of documentation across the projects vary. In 2022, the overall documentation effort was launched at the [DSS-Extentions hub](https://github.com/dss-extensions/dss-extensions) repository. The new websites, launched in 2024, are based on that.

This main site contains the topics listed at the end of the page. For documentation on specific projects, visit the specific links:

- **AltDSS engine/DSS C-API library:** For the low-level DSS C-API reference, there are files available at the [`docs`](https://github.com/dss-extensions/dss_capi/tree/master/docs) folder, and the [C header](https://github.com/dss-extensions/dss_capi/blob/master/include/dss_capi.h) itself is commented for most functions. A Doxygen documentation site covering the main DSS C-API header and the new dss.hpp classes is available at [https://dss-extensions.org/dss_capi/](https://dss-extensions.org/dss_capi/).
- **Our Python packages:** [DSS-Python](https://dss-extensions.org/DSS-Python/), [OpenDSSDirect.py](https://dss-extensions.org/OpenDSSDirect.py/) and [AltDSS-Python](https://dss-extensions.org/AltDSS-Python/) have dedicated docs.
- **OpenDSSDirect.jl:** [The Julia package has dedicated docs](https://dss-extensions.org/OpenDSSDirect.jl/stable/).
- **DSS_Sharp:** Includes integrated XML docs which are distributed with [the NuGet package](https://www.nuget.org/packages/dss_sharp/). A compiled site is available at [https://dss-extensions.org/dss_sharp/](https://dss-extensions.org/dss_sharp/). A step-by-step example is included in https://github.com/dss-extensions/dss_sharp/
- **[DSS_MATLAB](https://github.com/dss-extensions/dss_matlab/), [AltDSS-Go](https://github.com/dss-extensions/AltDSS-Go/), [AltDSS-Rust](https://github.com/dss-extensions/AltDSS-Rust/):** Includes partial help docs. Like DSS-Python, they have very good user-level API compatibility with the official COM implementation. As a result, the [official OpenDSS docs](https://opendss.epri.com/opendss_documentation.html) may help. Visit the target package repository for more.

An important reminder is that most of the original COM API functionality is exposed in most projects. As expected, the calling convention and general package organization does change from package to package. The API extensions, which include many extra functions and toggles, try to follow the conventions of each package. See the [known differences](https://github.com/dss-extensions/dss_capi/blob/master/docs/known_differences.md) document for an overview of the changes you can expected from using a DSS-Extensions project instead of the official OpenDSS.

Most of the documentation focuses on the API facet. For a reference of the OpenDSS commands and properties at script level, on the DSS basic scripting language, users can refer to the official OpenDSS documentation, or use [DSS-Extensions: OpenDSS Commands and Properties](https://github.com/dss-extensions/dss_capi/blob/master/docs/dss_properties.md) as a quick reference until we organize a general documentation covering important aspects of the projects listed here.

```{toctree}
:maxdepth: 2
:caption: General documentation
DSS Language <dss_language>
Classic API <classic_api>
Python APIs <python_apis>
Multithreading <multithreading>
licenses
```
