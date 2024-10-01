from typing import List

from fastapi import Depends, FastAPI, Body, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from database.orm import ToDo
from database.repository import create_todo, delete_todo, get_todo_by_todo_id, get_todos, update_todo
from schema.response import ToDoSchema, ToDoListSchema
from schema.request import CreateTodoRequest

app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"status": "ok"}



# todo_data = {
#     1: {
#         "id": 1,
#         "contnets": "todo test",
#         "is_done": True,
        
#     },
#     2: {
#         "id": 2,
#         "contnets": "todo test 1",
#         "is_done": False,
        
#     },
#     3: {
#         "id": 3,
#         "contnets": "todo test 2",
#         "is_done": False,
        
#     },
# }

@app.get("/todos", status_code=200)
def get_todos_handler(
    order: str | None = None,
    session: Session = Depends(get_db),
    ):
    
    todos: List[ToDo] = get_todos(session=session)
    if order and order == "DESC":
        return ToDoListSchema(
        todos=[
            ToDoSchema.from_orm(todo) for todo in todos[::-1]
        ]
        )
    return ToDoListSchema(
        todos=[
            ToDoSchema.from_orm(todo) for todo in todos
        ]
    )
    
    # ret = list(todo_data.values())
    # if order and order == "DESC":
    #     return ret[::-1]
    # return ret

@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(
    todo_id: int,
    session: Session = Depends(get_db),
    ) -> ToDoSchema:
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo not found")
    
    # todo = todo_data.get(todo_id)
    # if todo:
    #     return todo
    # return HTTPException(status_code=404, detail="Todo not found")

@app.post("/todos", status_code=201)
def create_todo_handler(
    request: CreateTodoRequest,
    session: Session = Depends(get_db),):
    todo: ToDo = ToDo.create(request=request)
    todo: ToDo = create_todo(session=session, todo=todo)
    
    return ToDoSchema.from_orm(todo)
    # todo_data[request.id] = request.dict()
    # return todo_data[request.id]

@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
        todo_id: int,
        is_done: bool = Body(..., embed=True),
        session: Session = Depends(get_db),
    ):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if todo:
        todo.done() if is_done else todo.undone()
        todo: ToDo = update_todo(session=session, todo=todo)
        return ToDoSchema.from_orm(todo)
    raise HTTPException(status_code=404, detail="Todo not found")
    # todo = todo_data.get(todo_id, {})
    # if todo:
    #     todo["is_done"] = is_done
    #     return todo
    # raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(
    todo_id: int,
    session: Session = Depends(get_db),
    ):
    todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    delete_todo(session=session, todo_id=todo_id)
    
    # todo = todo_data.pop(todo_id, None)
    # if todo:
    #     return
    # raise HTTPException(status_code=404, detail="Todo not found")