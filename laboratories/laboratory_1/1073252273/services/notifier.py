
from services.channel_factory import get_channel
from services.logger import Logger

def notify(user, message, priority="normal"):
    logger = Logger()
    channels = [user.preferred_channel] + [c for c in user.available_channels if c != user.preferred_channel]

    for ch in channels:
        channel_instance = get_channel(ch)
        logger.log(f"Attempting {ch} for user {user.name}")
        if channel_instance.send(user, message):
            logger.log(f"Success via {ch}")
            return True
        else:
            logger.log(f"Failed via {ch}")
    
    logger.log("All channels failed")
    return False
