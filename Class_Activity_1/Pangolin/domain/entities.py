import uuid
from dataclasses import dataclass

@dataclass
class Task:
    id: str
    title: str
    done: bool = False

    def mark_done(self):
        self.done = True
