from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"Message": "Hello World"}

@app.get("/{name}")
def greet_name(name: str, age: Optional[int] = None):
    return {"Message": f"Hello {name}"}

class Student(BaseModel):
    name: str
    age: int
    role: int

@app.post("/create_student")
def create_student(student: Student):
    return {
        "name": student.name,
        "age": student.age,
        "role": student.role,
    }
