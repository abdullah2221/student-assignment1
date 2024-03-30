from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()


class StudentInput(BaseModel):

    name: str
    age: int
    Grade: str


class StudentOut(StudentInput):
    student_Id: int = Field(..., gt=0)


students_Data: list[StudentOut] = []


@app.post('/students')
async def add_student(student: StudentInput) -> StudentOut:
    student_out = StudentOut(**student.model_dump(),student_Id=len(students_Data)+1)
    students_Data.append(student_out)
    return student_out


@app.get("/students")
def read_all_students() -> list[StudentOut]:
    return students_Data


@app.get('/students/{std_id}')
async def get_student(std_id: int) -> StudentOut | dict:
    for std in students_Data:
        if std.student_Id == std_id:
            return std
    return {"msg": "Student not found"}


@app.put("/students/{std_id}")
async def update_student(std_id: int, student: StudentInput) -> StudentOut | dict:
    for index, std in enumerate(students_Data):
        if std.student_Id == std_id:
            students_Data[index] = StudentOut(**student.model_dump(), student_Id=std_id)
            return students_Data[index]
    return {"msg": "Student not found"}

@app.delete('/students/{std_id}')
async def delete_student(std_id: int)->dict:
    for std in students_Data:
        if std.student_Id == std_id:
            students_Data.remove(std)
            return {"message": f"Student with ID {std_id} has been deleted"}
    return {"message": "Student not found"}
