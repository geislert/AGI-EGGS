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
on port `8766`. Each node sends a greeting message to the other and demonstrates
a broadcast, where one node sends a message to all of its connected peers.

## Frontend CLI

You can interact with nodes using `frontend.py`. The script starts a node
with a simple text interface for sending messages or broadcasting to all peers.

```
python3 frontend.py mynode --port 9000 --connect localhost:8765
```

Type commands like:

```
send greeting hello there
broadcast hello everyone
quit
```

`send` sends a message with a key to all connected peers, while `broadcast`
uses the network's broadcast feature. Incoming messages are printed to the
terminal.

## Offline message queue

Nodes can be created with a `MessageStore` to persist outgoing messages when
connections are unavailable. Queued messages are automatically flushed when a
new connection is made. This is useful for unreliable networks or disaster
recovery scenarios.

Example:

```python
from agi_eggs.node import PiNode
from agi_eggs.persistence import MessageStore

store = MessageStore("pending.jsonl")
pi = PiNode("pi-1", store=store)
```

Pending messages will be written to `pending.jsonl` and sent once peers
reconnect.

## Mesh example

The `mesh_example.py` script starts two Pi nodes and one Egg node, connecting
them in a small mesh network. Each node sends greetings and the egg broadcasts
a message to all peers.

```bash
python3 mesh_example.py
```

You should see output similar to:

```
[pi-2] received greeting from pi-1: hi from pi1
[egg-1] received greeting from pi-1: hi from pi1
[pi-1] received greeting from pi-2: hello from pi2
[egg-1] received greeting from pi-2: hello from pi2
[pi-1] received greeting from egg-1: greetings from egg
[pi-2] received greeting from egg-1: greetings from egg
[pi-1] broadcast from egg-1: mesh online
[pi-2] broadcast from egg-1: mesh online
```

This demonstrates simple information flow among multiple devices.
