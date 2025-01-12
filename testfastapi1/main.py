from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from models import ToDo, SessionLocal
from pydantic import BaseModel

app = FastAPI()

# Указываем, где искать статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Указываем, где искать HTML-шаблоны
templates = Jinja2Templates(directory="templates")

# Pydantic модели для запросов
class ToDoCreate(BaseModel):
    title: str
    description: str = None

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Главная страница (интерфейс)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Создание задачи
@app.post("/todos/", response_model=ToDoCreate)
def create_todo(todo: ToDoCreate, db: Session = Depends(get_db)):
    db_todo = ToDo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Получение всех задач
@app.get("/todos/")
def read_todos(db: Session = Depends(get_db)):
    return db.query(ToDo).all()

# Обновление задачи (например, пометить как выполненную)
@app.put("/todos/{todo_id}", response_model=ToDoCreate)
def update_todo(todo_id: int, todo: ToDoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="ToDo not found")

    db_todo.title = todo.title
    db_todo.description = todo.description
    db.commit()
    db.refresh(db_todo)
    return db_todo
