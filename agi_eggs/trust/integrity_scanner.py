class IntegrityScanner:
    SENSITIVITY = 0.7
    BASELINES = {}

    @classmethod
    def analyze_runtime_behavior(cls, component_id: str) -> float:
        # Dummy implementation
        baseline = cls.BASELINES.get(component_id, {"cpu_usage": 1.0})
        current = {"cpu_usage": 1.0}
        deviation = abs(current["cpu_usage"] - baseline["cpu_usage"])
        return max(0.0, 1 - deviation * cls.SENSITIVITY)

    @classmethod
    def adjust_sensitivity(cls, trust_level: float):
        cls.SENSITIVITY = 1.1 - trust_level
