# teasel instruments registry

Community-maintained (well, right now a community of one) registry of lab instrument descriptors for [teasel](https://teasel.tools) a tool for connecting lab instruments to AI assistants.

## What's in here

One TOML file per instrument. Each file describes the instrument, its interfaces, setup steps, and available MCP packages.

```
instruments/
├── pm5190.toml           # Philips PM5190 function generator
└── lecroy-wavesurfer.toml # LeCroy WaveSurfer oscilloscope
```

## Using the registry

Install [teasel](https://teasel.tools) and run:

```bash
uvx teasel add pm5190 --port /dev/ttyUSB0
```

## Adding an instrument

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Registry data (TOML files) is licensed under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)
