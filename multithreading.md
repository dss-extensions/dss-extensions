# DSS-Extensions: multiple DSS engines and multi-threading

**DRAFT**

<!--
- public language-specific examples
- finish updating OpenDSSDirect.jl
- finish DSS_MATLAB.mex
-->

# Architecture

**TODO**

# Linux-specific notes

To achieve safe multi-threading on Linux and macOS, there were a lot of small tweaks, and a big one: the memory allocator is now the system (C) allocator, instead of the default Free Pascal internal allocator.

Unfortunately, the default allocator on many Linux distributions does not work great for OpenDSS workloads.

To achieve better performance in general, both for single- and multi-threading, we recommend ensuring that a good allocator is used. We have tested a bunch of allocators and recommend the following two:

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

Effectively, using these allocators brings a lot more performance for DSS C-API 0.12+ than DSS C-API 0.10 or earlier with the internal allocator.
