
from fastapi import FastAPI, Body
from pydantic import BaseModel
from dboperations import getSingleData,insert,getAllData
from fastapi.responses import JSONResponse

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
            return JSONResponse(status_code=200,content={"data":response})
        else:
            return JSONResponse(status_code=401,content={"message":"Invalid Password"})
    return JSONResponse(status_code=401,content={"data":"Invalid username"})

@obj.post("/register")
def userRegistration(request:NewUserRequest):

    # check email exist
    email_status =  checkEmailExist(request.email)
    if email_status==True:
        return JSONResponse(status_code=400,content={"data":"email already exist"}) 

    # check mobile exist
    mobile_status =  checkMobileExist(request.mobile)
    if mobile_status==True:
        return JSONResponse(status_code=400,content={"data":"mobile already exist"})

    # check password match
    if request.password!=request.confirmed_password:
        return JSONResponse(status_code=400,content={"data":"password and confirm password should be same"})

    query = f"INSERT INTO user_login (name, email, mobile, password, role) VALUES ('{request.name}', '{request.email}', '{request.mobile}', '{request.password}', '{request.role}')"
    db_response = insert(query)
    if db_response is not None:
        return JSONResponse(status_code=201,content={"data":"User registered successfully"}) 

    return JSONResponse(status_code=500,content={"data":"something went wrong"}) 


@obj.get("/get-all-users")
def getAllUsers():
    query = "select * from user_login"
    db_response = getAllData(query)
    if db_response is not None:
        if len(db_response)>0:
            users_list = []
            for data in db_response:
                response = {
                                "id":data[0],
                                "name":data[1],
                                "email":data[2],
                                "mobile":data[3],
                                "role":data[5],
                                }
                users_list.append(response)
            return JSONResponse(status_code=200,content={"data":users_list}) 
        else:
            return JSONResponse(status_code=404,content={"data":"no records found"})
    else:
        return JSONResponse(status_code=500,content={"data":"something went wrong"})

@obj.get("/user-by-email")
def getUsersByEmail(email):
    query = f"select * from user_login where email='{email}'"
    db_response = getSingleData(query)
    if db_response is not None:
        response = {
                        "id":db_response[0],
                        "name":db_response[1],
                        "email":db_response[2],
                        "mobile":db_response[3],
                        "role":db_response[5],
                        }
        return JSONResponse(status_code=200,content={"data":response}) 
    else:
        return JSONResponse(status_code=404,content={"data":"no records found"}) 

@obj.get("/access-account")
def getUsersByEmail(email):
    query = f"select * from user_login where email='{email}'"
    db_response = getSingleData(query)
    if db_response is not None:
        if db_response[5]=="admin":
            return JSONResponse(status_code=200,content={"data":"Account Report Shared"})
        else:
             return JSONResponse(status_code=403,content={"data":"Not allowed to access resources"})
    else:
        return JSONResponse(status_code=404,content={"data":"no records found"}) 

@obj.get("/user-by-id/{id}")
def getUsersById(id):
    query = f"select * from user_login where id={id}"
    db_response = getSingleData(query)
    if db_response is not None:
        response = {
                        "id":db_response[0],
                        "name":db_response[1],
                        "email":db_response[2],
                        "mobile":db_response[3],
                        "role":db_response[5],
                        }
        return {"data":response}
    else:
        return {"data":"somethinf went wrong"}


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






