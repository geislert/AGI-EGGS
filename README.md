# AGI-EGGS: Asynchronous Gateway Interface - Experimental Grid System

A lightweight framework for building distributed IoT networks using asynchronous
message passing. Designed for educational demonstrations and prototyping
distributed systems.

![AGI-EGGS Network Diagram](https://example.com/agi-eggs-diagram.png)
<!-- Placeholder diagram above. Replace with an architecture image when available. -->

## Key Features
- **Node Communication**: Connect Raspberry Pi devices ("Pies") and experimental nodes ("Eggs").
- **Message Persistence**: Automatic offline message queuing with JSONL storage.
- **Broadcast Messaging**: One-to-many message propagation.
- **Real-time Monitoring**: Built-in CLI for network interaction.
- **Time-aware Operations**: Timestamped messages for event tracking.
- **Sensor Data Simulation**: Demonstrate real-world IoT scenarios.

## Getting Started

### Prerequisites
- Python 3.8+
- Raspberry Pi (optional for hardware demos)
- Basic knowledge of `asyncio`

### Installation
```bash
git clone https://github.com/geislert/AGI-EGGS.git
cd AGI-EGGS
pip install -r requirements.txt
```

## Basic Usage
Run the enhanced example:
```bash
python3 example.py
```
Sample output:
```
[2025-07-24T14:30:15.456] Connecting pi to egg...
[2025-07-24T14:30:15.567] raspberry-pi received: Hi from Sensor Egg!
[2025-07-24T14:30:15.572] Connecting egg to pi...
[2025-07-24T14:30:15.689] sensor-egg received: Hello from Raspberry Pi!
[2025-07-24T14:30:16.200] Pi broadcasting announcement...
[2025-07-24T14:30:16.751] Egg broadcasting sensor data...
Closing connections...
Networks stopped
```

## Interactive CLI Frontend
Monitor nodes in real time:
```bash
python3 frontend.py mynode --port 9000 --connect localhost:8765
```
Example session:
```
> send status_check Are you online?
< [2025-07-24T14:32:10.567] Received from pi-1: {"status": "online", "uptime": 120}
> broadcast sensor_update {"temp": 24.1, "hum": 43}
```

## Mesh Network Demo
Create a small mesh:
```bash
python3 mesh_example.py
```
Expected output:
```
[2025-07-24T14:35:22.101] pi-1 connected to egg-1
[2025-07-24T14:35:22.305] pi-2 connected to egg-1
[2025-07-24T14:35:23.100] egg-1 broadcasting network_status
```

## Message Persistence
Nodes queue outgoing messages when offline:
```python
from agi_eggs.node import PiNode
from agi_eggs.persistence import MessageStore

store = MessageStore("pending_messages.jsonl")
pi = PiNode("field-pi", store=store)
```
Messages are sent once peers reconnect.

## Real-world Applications
- **Disaster Monitoring**: Sensor networks with offline capability
- **Educational Kits**: Classroom IoT demonstrations
- **Research Prototyping**: Distributed system experiments
- **Home Automation**: Device coordination without cloud dependency

## Advanced Experimental Features
Several prototype modules extend AGI‑EGGS beyond basic networking. These modules
are optional and may require additional dependencies.

- **Architectural Conformance Agent**: audits actions against a simplified UDHR
  rule set.
- **Universal Unified Language Protocol**: encodes messages with provenance
  information for cross-module communication.
- **UULP Interpreter**: decodes and routes UULP messages between modules.
- **Quantum Secure Communications**: demonstrates Kyber-based encryption with a
  Fernet fallback.
- **Constitutional LLaMA**: wraps a language model with real-time ethics checks.
- **Trauma Detector**: placeholder workflow for mental health triage.
- **Rugged Edge Node**: describes hardware for off-grid deployment.
- **Humanitarian Data Governance**: sample GDPR-compliant data handler.
- **Geospatial Crisis Triage**: evaluate risk levels by ZIP code.
- **Self-Healing Data Provenance**: anchor dataset metadata for recovery.
- **Human-Like Search Agent**: fallback search strategy for crisis reports.
- **Autonomous Code Replacement**: prototype self-updater with rollback.
- **Offline Mesh Sync**: peer-to-peer sharing when internet fails.
- **Emergency Webhook**: dispatch urgent crisis alerts to chat platforms.

Use `from agi_eggs import *` to access these classes and consult the docstrings
for usage details. They currently provide demo functionality only.

See [ADVANCED_MODULES.md](docs/ADVANCED_MODULES.md) for a longer overview.
See [COMMUNICATION_PLAN.md](docs/COMMUNICATION_PLAN.md) for the proposed
low-cost global communication system.
See [HUMANITARIAN_INTEGRATION.md](docs/HUMANITARIAN_INTEGRATION.md) for notes on
connecting AGI-EGGS to existing aid and government platforms.
See [STRATEGIC_ENHANCEMENTS.md](docs/STRATEGIC_ENHANCEMENTS.md) for future high-impact feature ideas.

## Running Tests
Install test dependencies and run pytest:
```bash
pip install .[test]
pytest
```


## Contributing
We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License
GPL-3.0-or-later. See [LICENSE](LICENSE) for the full license text.
