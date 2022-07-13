This folder will contain [gettext](https://www.gnu.org/software/gettext/) translation files.

For the general messages from the DSS engine, these files are not required.

Starting in DSS C-API v0.12.0, the help/description of properties, command and options are not stored
in the source-code anymore. For those, one of the `.po` files here, after being compiled into the `.mo`
format, should be loaded through the `DSS_SetPropertiesMO` function from DSS C-API. This function should
be called once per process.

If you're embedding DSS C-API and do not need the help strings, you can safely ignore this, as it doesn't
affect the general program output, only the help descriptions and help commands.

As an initial step, the raw/original messages are being added to enable us to release DSS C-API v0.12.0.
Since the source-code is now decoupled from the help strings, we can incrementally merge other changes and
open the effort for community contributions. There is an on-going effort to reformat and enrich everything,
and also an effort to translate the text to Brazilian Portuguese. Please signal your interest in contributing
before working on this to avoid duplicated efforts. Other translations will be welcome when the 
infrastructure is in place (we will provide detailed instructions). We will also investigate using 
[Transifex](https://www.transifex.com/open-source/), for example.
