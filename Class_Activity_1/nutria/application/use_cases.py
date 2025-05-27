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
    
    # This method marks a task as done by its ID
    # It retrieves the task from the repository, marks it as done, and saves the updated task
    def mark_task_done(self, task_id: str) -> Task:
        try :
            task = self.repo.get_task_by_id(task_id)
            task.mark_done()
            self.repo.update(task)  # Update the task in the repository
            return task
        except ValueError as e:
            raise ValueError(f"Task with id {task_id} not found") from e