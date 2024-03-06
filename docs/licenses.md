# Licenses

The main licenses are BSD. Since this site itself is based on the OpenDSS and AltDSS, the licenses follow below.

## OpenDSS License

This is the main license of OpenDSS.

```{include} licenses/OPENDSS_LICENSE
   :literal:
```

## AltDSS License

This is the main license of the AltDSS/DSS C-API library. Same as the one from OpenDSS, but different authors.

```{include} licenses/ALTDSS_LICENSE
   :literal:
```

## Other

Each subproject has dedicated a license, since they originate from multiple authors and real-world organizations (DSS-Extensions is just a *GitHub* organization). These licenses include BSD, MIT, Apache2, and some variations.

The fork of KLUSolve uses LGPL, as the original KLUSolve. KLU itself uses LGPL, Eigen too (with a template exception), so it makes sense to do the same since DSS-Extensions KLUSolve is a small wrapper to provide an API for the Pascal code.
