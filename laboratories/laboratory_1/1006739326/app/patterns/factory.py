from app.patterns.channel_handler import EmailHandler, SMSHandler, ConsoleHandler

def create_channel_chain(channels):
    # Mapeamos nombres a clases
    handler_map = {
        "email": EmailHandler,
        "sms": SMSHandler,
        "console": ConsoleHandler
    }

    if not channels:
        return None

    # Creamos el primer handler
    first_handler = handler_map[channels[0]]()
    current_handler = first_handler

    # Encadenamos el resto
    for channel_name in channels[1:]:
        next_handler = handler_map[channel_name]()
        current_handler.set_next(next_handler)
        current_handler = next_handler

    return first_handler
