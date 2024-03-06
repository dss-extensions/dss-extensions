---
sd_hide_title: true
---
# Projects

These are several projects hosted and developed under DSS-Extensions.

![](https://raw.githubusercontent.com/dss-extensions/dss-extensions/master/images/repomap.png)

The code engine code and API is hosted in the [AltDSS/DSS C-API library](https://github.com/dss-extensions/dss_capi/). The code from the official OpenDSS SVN repository, hosted at [electricdss](https://sourceforge.net/p/electricdss/code/HEAD/tree/) on SourceForge.net, is tracked and relevant changes are ported to DSS C-API. A filtered copy, containing only source code files, is provided on GitHub on the [opendss-official-svn branch](https://github.com/dss-extensions/dss_capi/tree/opendss-official-svn) of the DSS C-API repository. The AltDSS C interface tries to be feature compatible with the COM interface from the official OpenDSS distribution. What was initially intended as a API-only project has evolved to contain many customizations and extensions.

:::{note}
DSS C-API is **not** developed in C. It does provides C headers for easier consumption, but originally it was developed with the Free Pascal compiler, and there is an on-going port for C++ (potentially Rust could be used in the long term). C is the lingua franca of interfaces (FFI), with good support from many other programming languages.
:::

The sparse solver used in OpenDSS, [KLUSolve](https://sourceforge.net/projects/klusolve/), was rewritten in the [DSS-Extensions fork of KLUSolve](https://github.com/dss-extensions/klusolve). It includes some extra code required by some of the AltDSS features, like incremental Y matrix updates, reuse of factorization, etc. The KLUSolve fork on DSS-Extensions uses [SuiteSparse's KLU](https://github.com/DrTimothyAldenDavis/SuiteSparse/) (as the original), and [Eigen](https://eigen.tuxfamily.org/) (original development). The plan is to merge the KLUSolve fork into AltDSS/DSS C-API in the future.

The discussion pages, general issue tickets, the main website, general assets including images and message catalogs and future internationalization, are hosted at the [hub repository `dss-extensions`](https://github.com/dss-extensions/dss-extensions).

There are slightly modified tests and examples from the official OpenDSS distribution in the [electricdss-tst repository](https://github.com/dss-extensions/electricdss-tst). If you have the official OpenDSS installed, most of the files in this repo should already be available in your machine. The files in the repo have been edited to avoid path issues on Linux and macOS.

Lastly, the language bindings expose the engine to the target languages. If you find yourself in need of a certain feature, feel free to open an issue in the respective repository, or in the hub repository (either in the [Discussions page](https://github.com/orgs/dss-extensions/discussions) or as a new issue, whichever seems to fit better).

## Classic API 

:::{seealso}
[What is *classic* API?](#classic_api)
:::

The following language specific extensions mimic the `COM` interface very closely. As such, they can be used as drop-in replacements for code that already uses the official COM module on Windows, enabling multi-platform usage.

- [DSS-Python](https://dss-extensions.org/DSS-Python): classic Python interface
- [DSS_MATLAB](https://github.com/dss-extensions/dss_matlab): MATLAB interface
- [DSS_Sharp](https://github.com/dss-extensions/dss_sharp): C#/.NET interface

Additionally, OpenDSSDirect interfaces have been built on top of DSS C-API and the language extensions. These `opendssdirect` or `odd`, until 2018, used the official OpenDSSDirect.DLL (on Windows), hence their names and some of the conventions used. See the following for more information:

- [OpenDSSDirect.py](https://github.com/dss-extensions/OpenDSSDirect.py) (Python)
- [OpenDSSDirect.jl](https://github.com/dss-extensions/OpenDSSDirect.jl) (Julia)


The following are new additions to DSS-Extensions. They also try to follow closely the organization of the official COM object, but are adapted to the target languages:

- [AltDSS-Go](https://github.com/dss-extensions/AltDSS-Go): Go ("golang") interface package; based on CGo.
- [AltDSS-Rust](https://github.com/dss-extensions/AltDSS-Rust): Rust interface package.

Another recent new addition is the `dss.hpp` C++ header library. It exposes the DSS C-API functions in an organized set of classes. A namespace `dss::classic` contains an organization that resembles the organization provided by the official COM implementation, and the new `dss::obj` interface (which will be renamed to `dss::alt` in the next release). It is currently hosted within the [DSS C-API](https://github.com/dss-extensions/dss_capi) repository.

## Alternative API

A new approach has been adopted to develop the new package [`AltDSS-Python`](https://dss-extensions.org/AltDSS-Python/). This package tries to expose all DSS objects, with the goal of providing a complete API to manipulate, create and export data from the DSS engine, doing away with the "Active..." mechanism used in the classic API. It can be used in conjunction to DSS-Python and/or OpenDSSDirect.py.

:::{note}
Originally, AltDSS-Python was intended to replace or extend OpenDSSDirect.py. See the project's website for more on the motivation for creating a new package.
:::

Lessons learned from this new project will guide the development of similar APIs for other programming languages. Most of the new features are expected to be ported to C++, Julia, and Rust, but there is no time table yet. 

In the low-level API, the Alternative API is mostly represented by the function families `Obj_*`, `Batch_*`, and `Alt_*`.
