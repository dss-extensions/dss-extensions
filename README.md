# DSS Extensions: hub repository

**This repository will be populated throughout July-August 2022. Check back regularly or use the "Watch" feature on GitHub to keep up-to-date.**

This GitHub repository will be used to concentrate documentation, discussions, benchmark results, and i18n/locale files around all projects hosted in the DSS Extensions organization. *As a reminder, the projects hosted here are not supported by EPRI.*

DSS Extensions were originally meant to expose the official OpenDSS engine to multiple languages and platforms with minimal changes. 
Since 2019, that goal has been reached and the target moved to modernize the our base library (DSS C-API) and add useful extensions and modifications to the DSS engine.

Projects currently hosted on this organization use several languages (Pascal, C, C++, Python, Julia, C#, MATLAB) and there have been requests and comments from users interested language bindings for other languages like Java, Go, and Rust. 
To avoid upsetting one of the language bindings when updating the base library, sometimes we cannot change certain aspects of the current implementation. This is the place to raise concerns and suggestions about such topics.

Several pre-2022 issues from the other projects were transferred to the issue tracker here. Even though the wording on those may suggest the original project/language, they present challenges or tasks shared across all projects.

Although we have the Discussions feature is enabled, there is no intention in fragmenting the OpenDSS community. We recommend checking and considering posting to the official OpenDSS forum if it's a general OpenDSS question or issue (if possible, test with the official OpenDSS GUI or using the official COM version).
- Official OpenDSS discussions: https://sourceforge.net/p/electricdss/discussion/
- Official OpenDSS docs at https://sourceforge.net/p/electricdss/code/HEAD/tree/trunk/Version8/Distrib/Doc/ and [OpenDSS_COM.chm](https://sourceforge.net/p/electricdss/code/HEAD/tree/trunk/Version8/Distrib/x64/OpenDSS_COM.chm?format=raw)
- Better search: use a search engine such as Google with `inurl:https://sourceforge.net/p/electricdss/discussion/` and your keywords; [example](https://www.google.com/search?q=inurl%3Ahttps%3A%2F%2Fsourceforge.net%2Fp%2Felectricdss%2Fdiscussion%2F+DSS+Extensions).


## API Documentation

Currently we have:

- [DSS C-API Pascal docs](https://dss-extensions.org/dss-extensions/pascal/): Documentation generated from the Pascal source code using PasDoc. This could be useful for someone studying the OpenDSS internals, especially of our implementation. [The class diagram](http://dss-extensions.org/dss-extensions/pascal/GVClasses.svg) is especially useful.
- [DSS C-API headers and dss.hpp](https://dss-extensions.org/dss_capi/): Documentation generated from the C headers and the new (WIP but quite extensive) C++ header library, including the classic API and the newest API extensions.
- [DSS-Python reference](https://dss-extensions.org/dss_python/): Minor notes and API docs; besides the classic API, this includes initial docs of the new Obj API.
- [DSS Sharp reference](https://dss-extensions.org/dss_sharp/): General API docs generated by the Sandcastle Help File Builder.
- [OpenDSSDirect.jl](https://dss-extensions.org/OpenDSSDirect.jl/stable/): Minor notes and API docs; needs some updates.
- [OpenDSSDirect.py](https://dss-extensions.org/OpenDSSDirect.py/): Minor notes and API docs; needs some updates.

For DSS_MATLAB, MATLAB itself can generate the docs using the [`help` function](https://www.mathworks.com/help/matlab/ref/help.html).

## FAQ

**1. Is this a toy project?**

**No.** This is a set of mature projects. The main developers and contributors are researchers or work in the industry. The results of our DSS engine are cross-validated with the official OpenDSS engine on a regular basis.

As a group, most of the projects were consolidated in 2018 and 2019.

Remember that version numbers are arbitrary. It is more important to check a project's history than just consider a version tag. For example, most of the initial goals for DSS C-API were reached by version 0.10; since the opportunity to add and complement the library was available, the plan is to release v1.0 when most planned features are integrated and the API is stable.

**2. Is this supported by EPRI?**

**No.** Consider contacting EPRI's team if you need official EPRI support for OpenDSS.

**3. Is this based on EPRI's `OpenDSSDirect.DLL`, aka DCSL?**

**No.** This is a common misconception. 

You also don't need to install the official OpenDSS binaries to use DSS Extensions. We do recommend that new users try following the official guides and use the official version, at least to get an idea of how OpenDSS works.

The base library from DSS Extensions is DSS C-API. It uses an interface developed independently, with high performance in mind, within the limitations of the given Pascal framework. Neither DSS C-API nor the DSS Extensions group was ever based on OpenDSSDirect.DLL/DCSL.

At first, the code was heavily based on the original code from the OpenDSS COM DLL (`OpenDSSengine.DLL`), with many modifications to achieve the initial goals. By doing that, we managed to reach the goal of good compatibility with the COM implementation, sidestepping the many issues we found when trying to do the same using the official `OpenDSSDirect.DLL`. For public data points, consider that several bugs in the projects OpenDSSDirect.py and OpenDSSDirect.jl were automatically addressed when they were migrated from the official OpenDSSDirect.DLL to DSS C-API.

Through the years, most of the code of the **API** was slowly rewritten or refactored to include more error checks, more messages, and reduce code duplication. As of DSS C-API v0.12.x series, a lot of the OpenDSS **engine internals** has been replaced or refactored, so the work that goes into DSS Extensions is much more than "copy code from EPRI and recompile with Free Pascal". Even the KLUSolve library was rewritten to address our needs, hence the library file is `libklusolvex` in the past few years.

Some historical context is available in https://sourceforge.net/p/electricdss/discussion/861976/thread/525c13df/ and other posts in the official OpenDSS forum.

**4. Why two Python packages, "DSS-Python" and "OpenDSSDirect.py"?**

Mostly for historical reasons.

When DSS C-API was first developed at Unicamp/Brazil, DSS-Python (or "dss_python") was a requirement to allow platform-independent code. The same Python code was required to run with the official OpenDSS COM DLL, and the our new Python module. If there were any doubts about the results we obtained in our Linux-based cluster, the same batch of scenarios (e.g. thousands of Monte Carlo simulations) would be re-evaluated using the official version on a cluster of Windows desktop machines.

At the point DSS-Python and DSS C-API were publicly announced, OpenDSSDirect.py ("ODD.py" for short) already existed as a project hosted and used at NREL for some time. 

Implementation-wise, there are different set of conventions between the two modules. Mostly, DSS-Python mimics the COM implementation of OpenDSS, using (sometimes abusing) the concept of property to pass data. ODD.py is based on functions instead, and has a more flat organization of modules/classes.

Since 2018 we accrued many users, which can be seen from the PyPI download numbers. In the long term, we plan to keep at least minimal maintenance of the two packages, while providing an alternative, clean-slate package to expose more interesting and modern approaches.

Further comments and a table mapping OpenDSSDirect.py and DSS-Python/COM API functions is available on [DSS Extensions — OpenDSS: Overview of Python APIs](https://github.com/dss-extensions/dss-extensions/blob/main/python_apis.md).

See also https://sourceforge.net/p/electricdss/discussion/beginners/thread/8031cde60e/?limit=25#4aca/5791/8bbb

**5. What are some features from EPRI's OpenDSS not available under DSS Extensions?**

There is a document at [known_differences](https://github.com/dss-extensions/dss_capi/blob/master/docs/known_differences.md) listing more. Notably:

- DSS Extensions do not integrate with some of EPRI's Windows-only software, like the plotting tools ("OpenDSS Viewer" and the old `DSSView.exe`), OpenDSS-GIS and others. It seems most of these are also closed-source software and/or not freely available for the general community.

- A few components were not ported (yet) or removed due to lack of test cases and other concerns. We are always open to revisit those if there are enough requests from users.

- Plotting is not available for all DSS Extensions. We are implementing a plotting backend under DSS-Python as a proof of concept. Introducing plotting to every project is not a goal, but we may add at least some plotting to DSS_MATLAB, and potentially add examples of how it would be implemented to DSS_Sharp and OpenDSSDirect.jl.

- The diakoptics features are currently disabled. The plan is to reintroduce them soon after some internal changes. Check the issues on the DSS C-API repository for details.

**6. Is this open-source?**

**Yes,** every single package available on DSS Extensions is open-source. Most are even built openly on the cloud.

We have seen some confusing statements asserting that DSS Extensions is not open-source. There is nothing inheritly wrong with closed-source software, but DSS Extensions is an open-source effort which can be fully built using only open-source (Free Pascal, Clang, GCC, etc.) and/or free tools (Visual Studio Dev Tools can be used for some DLLs).

Although some of the development was achieved by using DSS Extensions on financially supported research projects, most of the effort to maintain and improve our DSS engine beyond the original OpenDSS version has been done in a voluntary basis, in hopes that the effort helps making the tools more accessible to various users.

**7. What are some features from DSS Extensions not available in EPRI's OpenDSS?**

Again, more at [known_differences](https://github.com/dss-extensions/dss_capi/blob/master/docs/known_differences.md). 

At lot of the features below are still being documented.

- Consistent support for Windows, macOS and Linux.

- Consistent support for Intel x86, x86-64, ARM32 (currently armv7) and ARM64 (aarch64).

- Besides the parallel-machine mechanism based on actors from the official OpenDSS, we also allow multiple independent DSS engines in a single process. This enables user-controlled threads and other interest use-cases. Since our PM implementation is based on this concept of independent engines, it tends to present less errors and is more flexible than the official implementation.

- For some components, our engine allows incremental updates to the system Y matrix, which can result in good performance gains.

- A more flexible system for loading load-shape data, which also allows using float32 loadshapes for saving memory.

- A new set of functions to load circuits from ZIP archives.

- Experimental functions to access all DSS data classes, including initial support for exporting JSON-encoded data.

- A lot of feature and configuration toggles, some for maintaining backwards compatibility with older versions or with the official OpenDSS APIs and internal implementation.

- Many new functions to expose some of the missing classes from the COM API, and many functions that were added to due requests from various users.

- More of the engine internals are exposed through APIs. This is required for experts to achieve high performance on some tasks.

- More error-checking in general, including small features like error backtraces to save the users some time.

**8. Can I please get some examples/documentation?**

Soon! This is one of our priorities.

**9. Why doesn't `<insert feature>` work?**

Some features are constrained to mirror the official implementation. For everything else, please consider reporting. If you can provide a simple test case, even better.
