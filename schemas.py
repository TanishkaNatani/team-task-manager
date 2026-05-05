from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str


# ✅ THIS WAS MISSING
class Login(BaseModel):
    username: str
    password: str


class ProjectCreate(BaseModel):
    name: str


class TaskCreate(BaseModel):
    title: str
    project_id: int
    user_id: int