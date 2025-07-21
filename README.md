# AGI-EGGS

A small framework that demonstrates message passing between networked devices.
It provides a simple interface for connecting different nodes such as
Raspberry Pi devices ("pies") and experimental "AGI eggs".

This project is experimental and intended for educational purposes. It does not
implement real quantum computing but shows how devices might share information
using Python and `asyncio`.

## Usage

Run `example.py` to start two nodes that exchange greeting messages.

```bash
python3 example.py
```

The code creates a `PiNode` listening on port `8765` and an `EggNode` listening
on port `8766`. Each node sends a greeting message to the other.
