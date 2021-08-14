from fastapi import FastAPI,Path
from typing import Optional
from pydantic import BaseModel


app = FastAPI()
#instance of FastAPI

#end point of api
#localhost/delete-user           => delete-user is end point of the communication channel

#common api methods
#GET -> get or return an information ,
# POST ->create something new in database,
# PUT -> update,
# DELETE -> delete data



students = {
    1:{
        "name" : "John",
        "age" : 17,
        "year" : "12"
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str


class UpdateStudent(BaseModel):
    name : Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

#localhost/get-students is url path to get students 
#but to get a particular student's data we need to specify path eg /1 or /2
 
@app.get("/")        # / is homepage 
def index():
    return {"name": "First Data"}

#@app.get("/get-student/{student_id}")   #path parameter
#def get_student(student_id : int):
 #   return students[student_id]
    
@app.get("/get-student/{student_id}")   #path parameter
def get_student(student_id : int = Path(None,description="Student ID Required",gt=0,lt=3)):
    return students[student_id]


#gt->greater than,ge->greater than equals to,le,lt ---> to check whether the data satisfies these conditions

#query-parameter ---> used to pass a value to url
#ex: google.com/results?search=Python      ---> here search(key)=Python(value) is query parameter

#in path parameter we need to pass value in {} but not required so in query parameter
@app.get("/get-by-name")
def get_student(*,name :Optional[str] = None, test:int):     #using Optional & None we can use blank query

#python does not allow required arguments after optional arguments
#but using * we can overcome this restricion
    for student_id in students:
        if students[student_id]["name"]  == name:    #right side name is name being passed as query
            return students[student_id]
    return {"Data" : "Not Found"}


#combining path and query parameter
@app.get("/get-by-nameandid/{student_id}")
def get_student(*,student_id : int ,name :Optional[str] = None, test:int):  
    for student_id in students:
        if students[student_id]["name"]  == name:  
            return students[student_id]
    return {"Data" : "Not Found"}

#creating path using post method
@app.post("/create-student/{student_id}")
def create_student(student_id : int , student : Student):  #creating new Student object
    if student_id in students:
        return {"Error" : "Student exists"}

    students[student_id] = student
    return students[student_id]

#it will create student with id=2 but on refreshing page it will be gone


#put method
@app.put("/update-student/{student_id}")
def update_student(student_id : int , student : UpdateStudent):
    #if here we use Student we will need to change to all data;not a good practice
    if student_id not in students:
        return {"Error" : "Student does not exist"}

    #students[student_id] = student  it will update as null for fields for which we didn't give value
  

    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.year != None:
        students[student_id].year = student.year



    return students[student_id]     


@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error" : "Student does not exist"}
    
    del students[student_id]
    return {"Message" : "Student deleted"}