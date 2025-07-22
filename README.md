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
2. Execute the script (options shown with defaults). The file has a
   shebang so it can also be run directly once it is marked as
   executable (`chmod +x validation_protocol.py`):
   ```bash
   ./validation_protocol.py --trials 100 --dim 10 --threshold 0.9
   ```
   - `--trials`: number of perturbation trials
   - `--dim`: dimension of the generated tensors
   - `--threshold`: correlation required for the validation to pass
   - `--seed`: random seed for reproducibility
   - Use `-h`/`--help` to see all available options

The script prints the correlation between predicted and measured Φ values
and reports whether the validation passed.

## Additional resources

The file `PLASMA_MEMORY.md` contains a short summary of recent laboratory work
on plasma-based information storage. These experiments demonstrate that dusty
plasmas can form large, stable Coulomb crystals with viscoelastic memory
properties. They provide a starting point for anyone interested in exploring
plasma computing further.

The document `QUANTUM_CAPACITOR.md` outlines a proposed design for a quantum
plasma energy-storage capacitor. It summarizes the key materials,
theoretical advantages, and open challenges for building such a device.
