"""Vector set of signals for which to gather data, plot, ... """


class Vectors:
    def __init__(self, data: str) -> None:
        self.data = list(set(data.split()))

    def list_out(self) -> List[str]:
        return [str(item) for item in self.data]

    def __add__(self, other: "Vectors") -> "Vectors":
        combined = self.data + other.data
        unique_combined = list(set(combined))
        return Vectors(" ".join(unique_combined))
