from abc import ABC,abstractmethod
from pathlib import Path
import json
import streamlit as st


database="school.json"  # main database
data={"student":[] ,"teacher":[]}  # copy database of "student.json"

if Path(database).exists():  # this is to copy data in database
    with open(database ,'r') as f:
        content=f.read()
        if content:
            data=json.loads(content)

def save():
    with open(database,"w") as f:
        json.dump(data,f,indent=4)



class person(ABC):

    @abstractmethod
    def get_role(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def show_details(self):
        pass

    @staticmethod
    def validate_email(email):
        if "@" in email and "." in email:
            return True
        else:
            return False

class students(person):

    def get_role(self):
        return "student"
    
    def register(self):
        name=input("enter your name: ")
        age=int(input("enter your age:"))
        roll_no= int(input("enter your roll_no: "))
        email=input("enter your mail: ")

        if not person.validate_email(email):   # email check statement
            print("invaild email")
            return 
        
        for i in data["student"]:   # roll no checking statement
            if i['roll_no'] == roll_no:
                print("student already exixts")
                return
        
        data['student'].append({
            "name": name,
            "age" : age,
            "email": email,
            "roll_no": roll_no,
            "grades": {}

        })
        save()
        print(f"student {name} registered")

    def show_details(self):
        roll_no=input("enter roll_no: ")
        for s in data['student']:
            if s['roll_no'] == roll_no:
                grades = s['grades']
                avg = sum(grades.values()) / len(grades) if grades else 0

                print(f"\n Name: {s['name']}")
                print(f" Roll nd {s['roll_no']}")
                print(f" Grades: {grades}")
                print(f" Average: {avg:.1f}")
                return
    
    def add_grades(self):
        roll_no=int(input("entre your roll_no: "))
        subject= input("subject: ")
        marks= float(input("enter marks: "))

        for i in data['student']:
            if i['roll_no']==roll_no:
                i['grades'][subject]=marks
                save()
                print("grades added successfully")
                return
        print("student not found")


class teachers(person):

    def get_role(self):
        return "teacher"
    
    def register(self):
        name=input("enter your name: ")
        age=int(input("enter your age:"))
        employee_id = input("enter your employee_ id: ")
        subject=input("subject: ")
        email=input("enter your mail: ")

        if not person.validate_email(email):   # email check statement
            print("invaild email")
            return 
        
        for i in data['teacher']:   # roll no checking statement
            if i['employee_id'] == employee_id:
                print("student already exixts")
                return
        
        data['teacher'].append({
            "name": name,
            "age" : age,
            "email": email,
            "employee_id": employee_id,
            "subject":subject,
        })

        save()
        print(f"Teacher {name} registered")

    def show_details(self):
        emp_id= input("Employee ID: ")
                      
        for t in data["teachers"]:
            if t["emp_id"] == emp_id:
                print(f"\n Name : {t['name']}")
                print(f" Subject: {t['subject']}")
                print(f" Emp ID: {t['emp_id']}")
                return
        print("Teacher not found.")

stud=students()
tech=teachers()

print("press 1 for register a student")
print("press 2 for register a teacher")
print("press 3 to add grades")
print("press 4 to show details of student")
print("press 5 to  show details of teacher")

choice= int(input("enter your choice: "))

if choice == 1:
    stud.register()

elif choice == 2:
    tech.register()

elif choice == 3:
    stud.add_grades()

elif choice == 4:
    stud.show_details()

elif choice == 5:
    tech.show_details()