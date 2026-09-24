
from fastapi import FastAPI, Body,Request
from pydantic import BaseModel
from dboperations import getSingleData,insert,getAllData
from fastapi.responses import JSONResponse
from jose import jwt
from datetime import datetime,timedelta,timezone

#--------------------------------
# pip install python-jose
# --------------------------------

class LoginRequest(BaseModel):
    username:str
    password:str

CLIENT_SECRET_KEY = "codeminescomputerinstitute"
ALGORITHM = "HS256"

# create object of FastAPI
obj=FastAPI()

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
            expiry_date = datetime.now(timezone.utc) + timedelta(minutes=2)
            user_respose = {"data":response,"exp":expiry_date} 
            token = jwt.encode(user_respose,CLIENT_SECRET_KEY,algorithm=ALGORITHM)
            return JSONResponse(status_code=200,content={"token":token})
        else:
            return JSONResponse(status_code=401,content={"message":"Invalid Password"})
    return JSONResponse(status_code=401,content={"data":"Invalid username"})

@obj.get("/get-all-users")
def getAllUsers(request:Request):
    try:
        auth_token = request.headers.get("Authorization")
        auth_token = auth_token.replace("Bearer ","")
        auth_data = jwt.decode(auth_token, CLIENT_SECRET_KEY,algorithms=[ALGORITHM])
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
    except Exception as e:
        return JSONResponse(status_code=401,content={"data":"Invalid token"})


@obj.get("/get-account-details")
def getAccountDetails(request:Request):
    try:
        auth_token = request.headers.get("Authorization")
        auth_token = auth_token.replace("Bearer ","")
        auth_data = jwt.decode(auth_token, CLIENT_SECRET_KEY,algorithms=[ALGORITHM])
        user_data = auth_data["data"]
        if user_data["role"]=="admin":
            return JSONResponse(status_code=200,content={"message":"account report fetched successfully"})
        else:
            return JSONResponse(status_code=403,content={"message":"Not authorised to access api"})
    except Exception as e:
        return JSONResponse(status_code=401,content={"data":"Invalid token"})
    