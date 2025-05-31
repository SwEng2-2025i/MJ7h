import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from http_handler import create_http_handler
from src.application.use_cases import UseCase
from src.models.memory import Memory

memory = Memory()
use_case = UseCase(memory)
app = create_http_handler(use_case)

if __name__ == "__main__":
    app.run(debug=True)
