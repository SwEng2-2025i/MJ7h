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
    
    # Crear un metodo para poner la tarea como completada
    def mark_task_done(self, task_id: str) -> Task:
        task = self.repo.get_by_id(task_id)
        if task:
            task.mark_done()
            return task
        raise ValueError(f"Task with id {task_id} not found")