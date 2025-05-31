from .email import EmailChannel
from .sms import SMSChannel
from .console import ConsoleChannel

# Este módulo construye una cadena de responsabilidad para manejar diferentes canales de comunicación en base a los 3 canales actuales disponibles
def build_chain(available_channels, preferred):
    handlers = {}
    for ch in set(available_channels):
        if ch == 'email':
            handlers['email'] = EmailChannel()
        elif ch == 'sms':
            handlers['sms'] = SMSChannel()
        elif ch == 'console':
            handlers['console'] = ConsoleChannel()
    # Si el canal preferido esta en la lista lo agregamos
    orden = []
    if preferred in available_channels:
        orden.append(preferred)
    # ahora agregamos los canales disponibles que no son el preferido
    for c in available_channels:
        if c != preferred:
            orden.append(c)
    # Construimos la cadena de responsabilidad
    head = handlers.get(orden[0])
    current = head
    # Si no hay un canal preferido, usamos el primero de la lista
    for ch in orden[1:]:
        h = handlers.get(ch)
        # si el canal existe, lo agregamos a la caden
        if h:
            current = current.set_next(h)
    return head