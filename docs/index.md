---
sd_hide_title: true
myst:
  html_meta:
    "description lang=en": |
      Top-level documentation for the DSS-Extensions organization of projects, with general information about the OpenDSS implementation, general OpenDSS/AltDSS documentation, and links to the separate projects.
html_theme.sidebar_secondary.remove: true
---

# DSS-Extensions

[DSS-Extensions](https://github.com/dss-extensions) enables cross-platform (Windows, Linux, macOS) multi-language interfaces and extensions for an alternative/community implementation of EPRI's [OpenDSS](http://smartgrid.epri.com/SimulationTool.aspx), based on extended DSS engine and APIs.
OpenDSS is an open-source distribution system simulator [distributed by EPRI](https://sourceforge.net/projects/electricdss/).

![](https://raw.githubusercontent.com/dss-extensions/dss-extensions/master/images/repomap.png)

The main project is the AltDSS engine/DSS C-API library, a customized port of the [original/upstream OpenDSS source code](https://sourceforge.net/p/electricdss/code/HEAD/tree/), exposed with a more traditional C API. Nowadays, the public code repository from the upstream OpenDSS is tracked and changes are ported as required.

The language bindings expose the engine to the target languages, currently supporting Python, Julia, MATLAB, C#/.NET, Rust, Go, C++. See the [Projects page](#projects) for more.

The projects are **100% free, open-source software**. Licenses vary from project to project.

For illustration purposes, there are very reduced samples in various of the supported languages of how to load a circuit, solve it, and finally read the complex voltage array. Please check the documentation or code repositories for more.

``````{tab-set}
`````{tab-item} Python

Three packages are available and can be used together: [DSS-Python](https://dss-extensions.org/DSS-Python/) (drop-in replacement for OpenDSS COM), [OpenDSSDirect.py](https://dss-extensions.org/OpenDSSDirect.py/) (uses function-calls instead of Python properties, has some extras), and [AltDSS-Python](https://dss-extensions.org/AltDSS-Python/) (**new** alternative: detailed, modern API exposing all DSS objects, batches and more). The basics are very similar, include many extensions, but AltDSS includes distinct features, while the other two are more intended for backwards compatibility:

```python
from dss import dss # DSS-Python
dss.Text.Command = 'redirect "sample_circuit.dss"' # or dss('redirect sample_circuit.dss')
dss.ActiveCircuit.Solution.Solve()
voltages = dss.ActiveCircuit.AllBusVolts

from opendssdirect import dss as odd # OpenDSSDirect.py
odd('redirect "sample_circuit.dss"')
odd.Solution.Solve()
voltages = odd.Circuit.AllBusVolts()

from altdss import altdss # AltDSS
altdss('redirect "sample_circuit.dss"')
altdss.Solution.Solve()
voltages = altdss.BusVolts()
```

By default, OpenDSS engine errors are mapped to Python exceptions. Support for DSS plot commands is available.

`````
`````{tab-item} Julia
For more, see [OpenDSSDirect.jl](https://dss-extensions.org/OpenDSSDirect.jl/). OpenDSS engine errors are mapped to Julia exceptions. Support for DSS plot commands is under development.

```julia
using OpenDSSDirect
dss("redirect 'sample_circuit.dss'")
Solution.Solve()
voltages = Circuit.AllBusVolts()
```
`````
`````{tab-item} MATLAB

For more, see [DSS_MATLAB](https://github.com/dss-extensions/dss_matlab/). Intended as a multi-platform drop-in replacement for the official COM object.

```matlab
dss = DSS_MATLAB.IDSS;
dss.Text.Command = 'redirect "sample_circuit.dss"';
dss.ActiveCircuit.Solution.Solve();
voltages = dss.ActiveCircuit.AllBusVolts;
```
`````
`````{tab-item} C#/.NET
[Available on NuGet as `dss_sharp`](https://www.nuget.org/packages/dss_sharp/). For more, see [the repo](https://github.com/dss-extensions/dss_sharp/) and [the docs](https://dss-extensions.org/dss_sharp/).
Intended as a multi-platform drop-in replacement for the official COM object.

```csharp
using dss_sharp;
//...
DSS dss = new DSS();
dss.Text.Command = "redirect 'sample_circuit.dss'";
dss.ActiveCircuit.Solution.Solve();
var voltages = dss.ActiveCircuit.AllBusVolts;
```

By default, OpenDSS engine errors are mapped to C# exceptions, but the behavior is configurable.
`````
`````{tab-item} Go
See instructions on [AltDSS-Go's repo](https://github.com/dss-extensions/AltDSS-Go/), including a [more complete sample](https://github.com/dss-extensions/AltDSS-Go/blob/main/examples/simple.go). Currently mimics the official COM object API layout, within what's possible in Go. OpenDSS engine errors are mapped to Go errors.

```go
import (
	"log"

	"github.com/dss-extensions/altdss-go/altdss"
)
func main() {
	dss := altdss.IDSS{}
	dss.Init(nil)
	err := dss.Text.Set_Command("redirect 'sample_circuit.dss'");
	if err != nil {
		log.Fatal(err)
	}
	err := dss.ActiveCircuit.Solution.Solve();
	if err != nil {
		log.Fatal(err)
	}
	voltages, err := dss.ActiveCircuit.AllBusVolts()
	if err != nil {
		log.Fatal(err)
	}
}
```
`````
`````{tab-item} Rust
See instructions on [AltDSS-Rust's repo](https://github.com/dss-extensions/AltDSS-Rust), including some samples. Currently mimics the official COM object API layout, within what's possible in Rust. OpenDSS engine errors are mapped to Rust errors with `Result`.

```rust
use altdss::common::{DSSError, DSSContext};
use altdss::classic::IDSS;

fn run_sample(dss: &IDSS) -> Result<(), DSSError> {
  dss.Command("redirect 'sample_circuit.dss'")?;
  dss.ActiveCircuit.Solution.Solve()?;
  let voltages = dss.ActiveCircuit.AllBusVoltages()?;
}
fn main() {
  let ctx = DSSContext::prime();
  let dss = IDSS::new(&ctx);
  run_sample(&dss).unwrap();
}
```
`````
``````


```{toctree}
:maxdepth: 3
:caption: Contents on this main site
projects
faq
docs
citations
```
