from dataclasses import dataclass

@dataclass
class Client:
    intents: int = 0
    cache_limit: int = 200