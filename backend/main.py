from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Base de données temporaire
tasks = []

# Modèle de tâche
class Task(BaseModel):
    id: int
    title: str
    done: bool

# Route pour récupérer toutes les tâches
@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

# Route pour ajouter une nouvelle tâche
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task

# Route pour modifier une tâche
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    for i, t in enumerate(tasks):
        if t.id == task_id:
            tasks[i] = task
            return {"message": "Task updated"}
    return {"error": "Task not found"}

# Route pour supprimer une tâche
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [t for t in tasks if t.id != task_id]
    return {"message": "Task deleted"}
