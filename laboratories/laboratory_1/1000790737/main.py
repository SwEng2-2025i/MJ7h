from flask import Flask
from typing import List

from domain.ports.notification_sender import INotificationSender

from application.services.strategy import RandomChoiceStrategy, RandomIntStrategy
from application.services.chain import ChainSender
from application.services.user_service import UserService
from application.services.notification_service import NotificationService

from adapters.outbound.logger import SimpleLogger
from adapters.outbound.in_memory_user_repo import InMemoryUserRepository
from adapters.outbound.channels import (
    EmailSender,
    SmsSender,
    AppNotificationSender,
    SmokeSignalSender,
    CarrierPigeonSender,
)

from adapters.inbound.flask_controller import register_routes


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Infraestructure setup
    user_repository = InMemoryUserRepository()
    logger = SimpleLogger.get_instance()

    # User service setup
    u_svc = UserService(user_repository)

    sms_sender = SmsSender(RandomChoiceStrategy(logger), u_svc)
    email_sender = EmailSender(RandomIntStrategy(logger), u_svc)
    app_notification_sender = AppNotificationSender(RandomIntStrategy(logger), u_svc)
    smoke_signal_sender = SmokeSignalSender(RandomChoiceStrategy(logger), u_svc)
    carrier_pigeon_sender = CarrierPigeonSender(RandomChoiceStrategy(logger), u_svc)

    all_senders: List[INotificationSender] = [
        sms_sender,
        email_sender,
        app_notification_sender,
        smoke_signal_sender,
        carrier_pigeon_sender,
    ]

    # Chain of Responsibility setup
    chain = ChainSender(available_senders=all_senders)

    # Notification service setup
    n_svc = NotificationService(
        sender_chain=chain,
        user_repository=user_repository,
        logger=logger,
    )

    register_routes(app, u_svc, n_svc)
    return app


if __name__ == "__main__":
    app = create_app().run(debug=True, host="0.0.0.0", port=5000)
