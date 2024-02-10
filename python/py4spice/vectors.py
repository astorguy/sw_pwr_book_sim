"""Vector set of signals for which to gather data, plot, ... """


class Vectors:
    def __init__(self, data: str) -> None:
        self.data = list(set(data.split()))

    def __str__(self) -> str:
        return " ".join(self.data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.data})"

    def list_out(self) -> list:
        return self.data

    def __add__(self, other: "Vectors") -> "Vectors":
        combined = self.data + other.data
        unique_combined = list(set(combined))
        return Vectors(" ".join(unique_combined))
