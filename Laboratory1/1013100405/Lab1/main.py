# run.py
from flask import Flask
from infrastructure.users_repo import InMemoryUserRepository
from routes.app_endpoints import create_app
from infrastructure.notifications_logger import InMemoryLoggerRepository

if __name__ == '__main__':
    repo = InMemoryUserRepository()
    logger = InMemoryLoggerRepository()
    app = create_app(repo, logger)
    app.run(debug=True)
