
from fastapi import FastAPI, Body
from pydantic import BaseModel
from dboperations import getSingleData,insert

# create object of FastAPI
obj=FastAPI()

class LoginRequest(BaseModel):
    username:str
    password:str

class NewUserRequest(BaseModel):
    name:str
    email:str
    mobile:str
    password:str
    confirmed_password:str
    role:str


@obj.post("/auth")
def userLogin(request:LoginRequest):
    query = f"select * from user_login where email='{request.username}'"
    db_response = getSingleData(query)
    if db_response is not None:
        if db_response[4]==request.password:
            response = {
                "id":db_response[0],
                "name":db_response[1],
                "email":db_response[2],
                "mobile":db_response[3],
                "role":db_response[5],
                }
            return {"data":response}
        else:
            return {"message":"Invalid Password"}
    return {"data":"Invalid username"}

@obj.post("/register")
def userRegistration(request:NewUserRequest):

    # check email exist
    email_status =  checkEmailExist(request.email)
    if email_status==True:
        return {"message":"email already exist"}

    # check mobile exist
    mobile_status =  checkMobileExist(request.mobile)
    if mobile_status==True:
        return {"message":"mobile already exist"}

    # check password match
    if request.password!=request.confirmed_password:
        return {"message":"password and confirm password should be same"}

    query = f"INSERT INTO user_login (name, email, mobile, password, role) VALUES ('{request.name}', '{request.email}', '{request.mobile}', '{request.password}', '{request.role}')"
    db_response = insert(query)
    if db_response is not None:
        return {"data":"User registered successfully"}

    return {"data":"something went wrong"}

def checkEmailExist(email):
    query = f"select * from user_login where email='{email}'"
    db_response = getSingleData(query)
    if db_response is None:
        return False
    else:
        return True 

def checkMobileExist(mobile):
    query = f"select * from user_login where mobile='{mobile}'"
    db_response = getSingleData(query)
    if db_response is None:
        return False
    else:
        return True 


