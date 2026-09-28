from fastapi import APIRouter, HTTPException, status
from models.model import Task, TaskInsert

task_router = APIRouter()

datas = [
  { "id": 0, "text": "Visit Kafka Museum", "done": True },
  { "id": 1, "text": "Watch a puppet show", "done": False },
  { "id": 2, "text": "Lennon Wall pic", "done": False },
]


tasks = [Task(**t) for t in datas]

@task_router.get("", response_model=list[Task])
async def get_tasks():
    return tasks

@task_router.post("")
async def post_task(data:TaskInsert) :
    new_id = max(task.id for task in tasks) + 1
    task = Task(id=new_id, text=data.text, done=data.done)
    tasks.append(task)
    return task

@task_router.put("/{id}")
async def put_task(id:int, update_task:Task):
    for task in tasks:
        if task.id == id:
            task.text = update_task.text
            task.done = update_task.done
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task를 찾을 수 없습니다.")

@task_router.delete("/{id}", response_model=list[Task])
async def delete_task(id:int):
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            return tasks
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task를 찾을 수 없습니다.")