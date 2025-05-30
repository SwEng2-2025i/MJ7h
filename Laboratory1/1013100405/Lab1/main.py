# run.py
from flask import Flask
from infrastructure.users_repo import InMemoryUserRepository
from routes.app_endpoints import create_app

if __name__ == '__main__':
    repo = InMemoryUserRepository()
    app = create_app(repo)
    app.run(debug=True)
