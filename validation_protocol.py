#!/usr/bin/env python3
"""Minimal Φ-Calculus validation demo.

This script generates synthetic tensors, perturbs them, and measures
how closely the observed system response correlates with a predicted
Φ value.  Parameters such as the number of trials, dimension of the
tensors and the pass/fail threshold can be supplied via command-line
arguments.
"""

from __future__ import annotations

import argparse
import numpy as np


def adversarial_perturbation(
    vec: np.ndarray,
    scale: float = 0.1,
) -> np.ndarray:
    """Return a small perturbation of ``vec``.

    Parameters
    ----------
    vec:
        Vector to perturb.
    scale:
        Standard deviation of the Gaussian noise.
    """

    noise = np.random.normal(scale=scale, size=vec.shape)
    return vec + noise


class SimpleSystem:
    """Simple linear system used for demonstration."""

    def propagate(
        self, probe: np.ndarray, noise_scale: float = 0.05
    ) -> np.ndarray:
        """Propagate ``probe`` through the system with optional noise."""

        noise = np.random.normal(scale=noise_scale, size=probe.shape)
        return probe + noise


def run_validation(
    dim: int,
    trials: int,
    threshold: float,
    seed: int = 0,
    domains: int = 1,
    weights: list[float] | None = None,
) -> float:
    """Run the validation protocol with optional multi-domain weighting.

    Parameters
    ----------
    dim:
        Dimension of the P and V vectors per domain.
    trials:
        Number of perturbation trials.
    threshold:
        Pass/fail correlation threshold.
    seed:
        Random seed for reproducibility.
    domains:
        Number of independent domains to combine.
    weights:
        Optional list of domain weights (will be normalized).

    Returns
    -------
    float
        Correlation coefficient across all trials.
    """

    rng = np.random.default_rng(seed)
    if weights is None:
        weights = [1.0 / domains] * domains
    if len(weights) != domains:
        raise ValueError("weights length must equal domains")
    total = sum(weights)
    weights = [w / total for w in weights]

    P = rng.standard_normal((domains, dim))
    V = rng.standard_normal((domains, dim))
    system = SimpleSystem()

    phi_predicted_values: list[float] = []
    phi_measured_values: list[float] = []

    for _ in range(trials):
        phi_pred_trial = []
        phi_meas_trial = []
        for d in range(domains):
            probe = adversarial_perturbation(P[d])
            response = system.propagate(probe)
            phi_predicted = np.dot(probe, V[d])
            phi_measured = np.dot(response, V[d])
            phi_pred_trial.append(phi_predicted)
            phi_meas_trial.append(phi_measured)
        phi_predicted_values.append(float(np.dot(weights, phi_pred_trial)))
        phi_measured_values.append(float(np.dot(weights, phi_meas_trial)))

    correlation = np.corrcoef(
        phi_predicted_values,
        phi_measured_values,
    )[0, 1]

    print(f"Correlation across {trials} trials: {correlation:.3f}")
    result = "passed" if correlation > threshold else "failed"
    print(f"Validation {result}")
    return correlation


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--trials",
        type=int,
        default=100,
        help="number of perturbation trials",
    )
    parser.add_argument(
        "--dim",
        type=int,
        default=10,
        help="dimension of tensors",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.9,
        help="correlation threshold for passing",
    )
    parser.add_argument(
        "--domains",
        type=int,
        default=1,
        help="number of independent domains",
    )
    parser.add_argument(
        "--weights",
        type=str,
        help="comma-separated domain weights (optional)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="random seed",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    weight_vals = None
    if args.weights:
        weight_vals = [float(w) for w in args.weights.split(",")]
    run_validation(
        args.dim,
        args.trials,
        args.threshold,
        seed=args.seed,
        domains=args.domains,
        weights=weight_vals,
    )


if __name__ == "__main__":
    main()
