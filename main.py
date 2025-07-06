from fastapi import FastAPI, BackgroundTasks, HTTPException
import uuid
from typing import Dict

app = FastAPI()
tasks: Dict[str, str] = {}  # task_id: status


def simulate_task(task_id: str):
    import time
    tasks[task_id] = "processing"
    time.sleep(3)  # simulate a task taking 3 seconds
    tasks[task_id] = "completed"


@app.post("/submit")
def submit_task(background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks[task_id] = "queued"
    background_tasks.add_task(simulate_task, task_id)
    return {"task_id": task_id}


@app.get("/status/{task_id}")
def get_status(task_id: str):
    status = tasks.get(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, "status": status}
