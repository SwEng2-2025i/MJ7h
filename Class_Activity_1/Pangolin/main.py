from application.use_cases import TaskUseCase
from adapters.memory_repo import InMemoryTaskRepository
from adapters.http_handler import create_http_handler

if __name__ == "__main__":
    repo = InMemoryTaskRepository()
    use_case = TaskUseCase(repo)
    app = create_http_handler(use_case)
    app.run(debug=True)