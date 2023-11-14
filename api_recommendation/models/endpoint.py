class Endpoint:
    endpoint: str
    description: str
    bow: list[str]

    def __init__(self, endpoint: str, description: str, bow: list[str] = []):
        self.endpoint = endpoint
        self.description = description
        self.bow = bow

    def __repr__(self):
        return f"Endpoint: {self.endpoint}"

    def __str__(self):
        return f"Endpoint: {self.endpoint}"



