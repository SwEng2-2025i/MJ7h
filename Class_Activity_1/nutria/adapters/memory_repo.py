from domain.ports import TaskOutputPort
from domain.entities import Task

class InMemoryTaskRepository(TaskOutputPort):
    def __init__(self):
        self.tasks = []

    def save(self, task: Task) -> None:
        self.tasks.append(task)

    def list_all(self) -> list[Task]:
        return self.tasks
        
    def get_task_by_id(self, task_id: str) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"Task with id {task_id} not found")
    
    # This method updates an existing task in the repository
    # It searches for the task by its ID and replaces it with the updated task
    # If the task is not found, it raises a ValueError
    def update_task(self, task: Task) -> None:
        for i, t in enumerate(self.tasks):
            if t.id == task.id:
                self.tasks[i] = task
                return
        raise ValueError(f"Task with id {task.id} not found")
