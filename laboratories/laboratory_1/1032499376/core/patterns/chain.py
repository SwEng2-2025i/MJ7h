# core/patterns/chain.py
from abc import ABC, abstractmethod
from random import random
from core.logger import EventLogger
from random import random
from typing import Set
from core.models import ChannelType, User
from core.models import Notification, ChannelType

log = EventLogger()



class ChannelHandler(ABC):

    def __init__(self):
        self._next: "ChannelHandler | None" = None

    def set_next(self, nxt: "ChannelHandler") -> "ChannelHandler":
        self._next = nxt
        return nxt  # permite encadenar llamadas .set_next(a).set_next(b)

    def handle(self, notification: Notification) -> bool:
        """Devuelve True si la entrega tuvo éxito,
        False si falló en este nodo y no hay más nodos."""
        if self._send(notification):
            return True
        if self._next:
            return self._next.handle(notification)
        return False

    @abstractmethod
    def _send(self, notification: Notification) -> bool:
        """Implementación concreta de envío.
        Debe devolver True si tuvo éxito, False si falló."""
        pass


# ------------- Handlers concretos --------------------------------- #
class EmailHandler(ChannelHandler):
    def _send(self, notification: Notification) -> bool:
        success = random() > 0.20          
        log.info(
            f"TRY  | notif={notification.id} | channel=EMAIL   | "
            f"result={'OK' if success else 'FAIL'}"
        )
        return success


class SMSHandler(ChannelHandler):
    def _send(self, notification: Notification) -> bool:
        success = random() > 0.10
        log.info(
            f"TRY  | notif={notification.id} | channel=SMS     | "
            f"result={'OK' if success else 'FAIL'}"
        )
        return success


class ConsoleHandler(ChannelHandler):
    def _send(self, notification: Notification) -> bool:
        log.info(
            f"TRY  | notif={notification.id} | channel=CONSOLE | result=OK"
        )
        print(f"Console log: {notification.message}")
        return True



# ------------- Factory Method (2º patrón) ------------------------- #
def handler_factory(channel: ChannelType) -> ChannelHandler:
    """Devuelve el handler apropiado según el tipo."""
    match channel:
        case ChannelType.EMAIL:
            return EmailHandler()
        case ChannelType.SMS:
            return SMSHandler()
        case ChannelType.CONSOLE:
            return ConsoleHandler()

# core/patterns/chain.py  (al final del archivo)

def build_chain_for(user: User) -> ChannelHandler:
    """Devuelve la cadena sin repetir canales.
    Orden: preferido → backups en el orden dado
    """
    first = handler_factory(user.preferred_channel)
    current = first

    seen: Set[ChannelType] = {user.preferred_channel}   # lleva registro

    for ch in user.backup_channels:
        if ch in seen:          # salta duplicados
            continue
        seen.add(ch)
        nxt = handler_factory(ch)
        current.set_next(nxt)
        current = nxt

    return first


