import numpy as np

"""Simple demonstration of a validation protocol for Φ-Calculus.
This script generates synthetic data to test whether the system's
response to perturbations correlates with predicted Φ values.
"""

np.random.seed(0)
P = np.random.randn(10)
V = np.random.randn(10)


def adversarial_perturbation(P):
    """Return a small perturbation of P."""
    noise = np.random.normal(scale=0.1, size=P.shape)
    return P + noise


class SimpleSystem:
    def propagate(self, probe):
        """Simple linear propagation with noise."""
        noise = np.random.normal(scale=0.05, size=probe.shape)
        return probe + noise


system = SimpleSystem()

num_trials = 100
phi_predicted_values = []
phi_measured_values = []

for _ in range(num_trials):
    probe = adversarial_perturbation(P)
    response = system.propagate(probe)
    phi_predicted_values.append(np.dot(probe, V))
    phi_measured_values.append(np.dot(response, V))

correlation = np.corrcoef(phi_predicted_values, phi_measured_values)[0, 1]

print(f"Correlation across {num_trials} trials: {correlation:.3f}")
print("Validation passed" if correlation > 0.9 else "Validation failed")
