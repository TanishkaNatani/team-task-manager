from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal, Base
from auth import create_token

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔐 SIGNUP
@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    return {"msg": "User created"}

# 🔑 LOGIN
@app.post("/login")
def login(user: schemas.Login, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_token({"user_id": db_user.id, "role": db_user.role})
    return {"access_token": token}

# 📁 CREATE PROJECT (Admin only)
@app.post("/project")
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    new_project = models.Project(name=project.name, owner_id=1)
    db.add(new_project)
    db.commit()
    return {"msg": "Project created"}

# 📌 CREATE TASK
@app.post("/task")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    return {"msg": "Task created"}

# 📊 DASHBOARD
@app.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    total = db.query(models.Task).count()
    completed = db.query(models.Task).filter(models.Task.status == "completed").count()
    pending = db.query(models.Task).filter(models.Task.status == "pending").count()
    return {
        "total_tasks": total,
        "completed": completed,
        "pending": pending
    }

# 🔄 UPDATE TASK
@app.put("/task/{task_id}")
def update_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    task.status = "completed"
    db.commit()
    return {"msg": "Task updated"}