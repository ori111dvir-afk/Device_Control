class Actuator:
    def activate(self, value: float) -> None:
        print(f"WARNING: filtered value {value:.2f} exceeded threshold!")
