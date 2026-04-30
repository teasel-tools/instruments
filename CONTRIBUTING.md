# Contributing

## Adding an instrument

1. Fork this repo
2. Copy `instruments/pm5190.toml` as a starting point
3. Save it as `instruments/{slug}.toml` where `slug` is lowercase with hyphens (e.g. `keysight-34401a.toml`)
4. Add an entry to `index.toml`
5. Open a PR. You file will automatically be validated by the CI (fingers crossed)

## Required fields

Every instrument TOML must have:

```toml
[instrument]
slug = "your-instrument-slug"   # must match the filename
name = "Make and Model"
manufacturer = "Make"
type = "oscilloscope"           # see types below

[[mcp.packages]]
package = "your-package-name"
distribution = "pypi"           # pypi | npm | cargo | homebrew | binary
install = "uvx your-package"
command = "uvx your-package"
```

## Instrument types

`oscilloscope`, `function-generator`, `multimeter`, `power-supply`, `spectrum-analyzer`, `signal-generator`, `function-generator`, `logic-analyzer`, `spectrum-analyzer`, `vector-network-analyzer`, `power meter`, `debugger`,`simulator`,`other`

This is just a list of the top of my head, so let me know what you want to add. I am not yet set on how to deal with "virtual" tools like a simulator. So, let's see where it goes. 

## What CI checks

- TOML is syntactically valid
- All required fields are present
- `slug` matches the filename
- At least one `[[mcp.packages]]` entry exists (right now only MCP is supported this might be extended later on)
- Each package exists on its declared distribution (PyPI, npm, Cargo)
- All URLs resolve (manual, images, package URLs)

## What you don't need to do

- You don't need to publish your package here. The registry only points to it.
- You don't need permission to list alternative implementations of the same instrument.
- No account, no backend: Just open a Pull request and it will be added. 
