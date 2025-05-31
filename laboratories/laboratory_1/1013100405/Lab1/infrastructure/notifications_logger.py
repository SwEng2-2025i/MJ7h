from domain.entities.log_entry import LogEntry

class InMemoryLoggerRepository:
    def __init__(self):
        self.logs = []

    def save(self, entry: LogEntry):
        self.logs.append(entry)

    def list_all(self) -> list[LogEntry]:
        return self.logs