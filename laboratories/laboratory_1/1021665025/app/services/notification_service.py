from typing import List, Dict, Optional
from app.models.user import User
from app.models.notification import NotificationPayload
from app.channels import CHANNEL_FACTORY, BaseChannel
from app.utils.logger import logger

# Almacenamiento en memoria para usuarios. La clave es el nombre del usuario.
users_db: Dict[str, User] = {}

class NotificationService:
    #Servicio para gestionar usuarios y enviar notificaciones.

    def register_user(self, name: str, preferred_channel: str, available_channels: List[str]) -> User:
        #Registra un nuevo usuario en el sistema.
        #Si el usuario ya existe, se actualizan sus datos.
        #Valida que los canales especificados sean válidos.

        #Retorna el objeto User creado o actualizado.
        #Lanza una excepción ValueError si se especifica un canal no válido o si el canal preferido no está en los canales disponibles.

        logger.info(f"Registrando usuario: {name} con canal preferido: {preferred_channel} y canales disponibles: {available_channels}")

        # Validar que todos los canales (preferido y disponibles) sean válidos
        valid_system_channels = CHANNEL_FACTORY.keys()
        if preferred_channel not in valid_system_channels:
            raise ValueError(f"Canal preferido no valido: '{preferred_channel}'. Canales validos: {list(valid_system_channels)}")
        for channel in available_channels:
            if channel not in valid_system_channels:
                raise ValueError(f"Canal disponible no valido: '{channel}'. Canales validos: {list(valid_system_channels)}")

        try:
            user = User(name, preferred_channel, available_channels)
            users_db[user.name] = user
            logger.info(f"Usuario '{user.name}' registrado/actualizado exitosamente.")
            return user
        except ValueError as e:
            logger.error(f"Error al registrar usuario '{name}': {e}")
            raise e # Re-lanza la excepción para que sea manejada por la API

    def get_all_users(self) -> List[User]:
        logger.info("Obteniendo lista de todos los usuarios.")
        return list(users_db.values())

    def _build_channel_chain(self, user: User) -> Optional[BaseChannel]:
        #Construye la cadena de responsabilidad de canales para un usuario específico.

        #La cadena se ordena comenzando por el canal preferido del usuario,
        #seguido por los otros canales disponibles, en el orden en que aparecen

        if not user.available_channels:
            logger.warning(f"Usuario '{user.name}' no tiene canales disponibles. No se puede construir la cadena.")
            return None

        ordered_channel_names = [user.preferred_channel]
        for ch_name in user.available_channels:
            if ch_name != user.preferred_channel and ch_name not in ordered_channel_names:
                ordered_channel_names.append(ch_name)
        
        logger.debug(f"Orden de canales determinado para '{user.name}': {ordered_channel_names}")

        head_channel: Optional[BaseChannel] = None
        current_channel: Optional[BaseChannel] = None

        for channel_name in ordered_channel_names:
            channel_class = CHANNEL_FACTORY.get(channel_name)
            if channel_class:
                new_channel_instance = channel_class()
                if head_channel is None: # Primer canal en la cadena
                    head_channel = new_channel_instance
                    current_channel = head_channel
                else: # Enlazar al canal anterior
                    if current_channel: # Chequeo para mypy
                         current_channel.set_next(new_channel_instance)
                    current_channel = new_channel_instance # Mover al nuevo canal para el siguiente enlace
            else:
                logger.warning(f"No se encontro la clase para el canal '{channel_name}' en CHANNEL_FACTORY.")
        
        if head_channel:
            chain_str = head_channel.channel_name()
            next_in_chain = head_channel._next_channel
            while next_in_chain:
                chain_str += f" -> {next_in_chain.channel_name()}"
                next_in_chain = next_in_chain._next_channel
            logger.info(f"Cadena de canales construida para '{user.name}': {chain_str}")
        else:
            logger.warning(f"No se pudo construir ninguna cadena de canales para '{user.name}'")

        return head_channel

    def send_notification(self, payload: NotificationPayload) -> Dict[str, any]:
        #Envía una notificacion a un usuario.
        #Busca al usuario por su nombre. Si existe, construye su cadena de canales e intenta enviar la notificacion. 

        #Retorna un diccionario con el estado del envío:
        #{ "status": "enviada" | "fallo_usuario_no_encontrado" | "fallo_sin_canales" | "fallo_envio", "message": "Mensaje descriptivo" }
        
        logger.info(f"Solicitud de notificacion recibida para '{payload.user_name}' con mensaje: '{payload.message}' y prioridad: '{payload.priority}'")
        user = users_db.get(payload.user_name)

        if not user:
            logger.error(f"Usuario '{payload.user_name}' no encontrado para enviar notificacion.")
            return {"status": "fallo_usuario_no_encontrado", "message": f"Usuario '{payload.user_name}' no encontrado."}

        channel_chain_head = self._build_channel_chain(user)

        if not channel_chain_head:
            logger.error(f"No se pudo construir la cadena de canales para el usuario '{user.name}'. Notificacion no enviada.")
            return {"status": "fallo_sin_canales", "message": f"Usuario '{user.name}' no tiene canales configurados o validos."}

        logger.info(f"Iniciando envio de notificacion para '{user.name}' a través de la cadena de canales (iniciando con {channel_chain_head.channel_name()})...")
        if channel_chain_head.send(user.name, payload.message):
            logger.info(f"Notificacion para '{user.name}' enviada exitosamente a través de la cadena.")
            return {"status": "enviada", "message": f"Notificacion para '{user.name}' procesada. Verifique los logs para el resultado final del canal."}
        else:
            logger.error(f"Todos los canales fallaron al enviar la notificacion para '{user.name}'.")
            return {"status": "fallo_envio", "message": f"Notificacion para '{user.name}' no pudo ser enviada a través de ningún canal."} 