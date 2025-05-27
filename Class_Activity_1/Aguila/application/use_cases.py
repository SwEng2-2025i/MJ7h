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
    # Añadimos la funsion mark_task_done, la cual busca una tarea por su id
    # Si la tarea no existe, se lanza un ValueError
    # Si la tarea existe, se marca como completada y se guarda en el repositorio
    def mark_task_done(self, task_id: str) -> Task:
        task = self.repo.get_by_id(task_id)
        if task is None:
            raise ValueError(f"Task with id {task_id} not found")
        task.mark_done()
        self.repo.save(task)
        return task
