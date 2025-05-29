import uuid
from domain.entities import Task
from domain.ports import TaskInputPort, TaskOutputPort

class TaskUseCase(TaskInputPort):
    def __init__(self, repo: TaskOutputPort):
        self.repo = repo

    def create_task(self, title: str) -> Task:
        task = Task(id=str(uuid.uuid4()), title=title)
        self.repo.save(task)
        return task

    def get_all_tasks(self) -> list[Task]:
        return self.repo.list_all()

    def mark_done(self, id: str) -> Task:
        task = self.repo.get_by_id(id)
        if (task is None):
            raise ValueError(f"task not found")
        task.mark_done()
        self.repo.save(task)
        return task
        
