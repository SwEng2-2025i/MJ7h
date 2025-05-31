class NotificationService:
    def __init__(self, channels):
        for i in range(len(channels) - 1):
            channels[i].set_next(channels[i + 1])
        self.chain = channels[0] if channels else None

    def send(self, preferred, message):
        if not self.chain:
            return {"status": "failed", "message": "No channels available."}
        return self.chain.handle(preferred, message)