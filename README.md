# AGI-EGGS

This repository contains a minimal prototype demonstrating a simple
"validation protocol" inspired by the Φ-Calculus concept. The script
`validation_protocol.py` generates synthetic tensors, applies small
perturbations, and measures whether the predicted boundary response
correlates with the observed system behavior.

## Running the demo
1. Install the only dependency (NumPy):
   ```bash
   pip install numpy --user
   ```
2. Execute the script:
   ```bash
   python3 validation_protocol.py
   ```
The script prints the correlation between predicted and measured Φ values
across multiple trials.
