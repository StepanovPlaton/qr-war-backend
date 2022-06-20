#!/usr/bin/python

from fastapi import FastAPI, HTTPException
import uvicorn #type: ignore

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[0]))

from utils.YAMLReader import YAMLReaderClass
from utils.ConfigReader import ConfigClass
from utils.Logger import LoggerClass
from utils.DatabaseFriend import *
from utils.Hasher import HasherClass
from utils.Models import *

YAMLReader = YAMLReaderClass()
Config = ConfigClass(YAMLReader)
Logger = LoggerClass(Config)
Hasher = HasherClass()
DatabaseFriend: DatabaseFriendClass | None = None

app = FastAPI()

@app.on_event("startup") #type: ignore
async def startup():
    global DatabaseFriend

    Logger.Log("Server startup - OK")
    DatabaseFriend = DatabaseFriendClass(Config, Logger, Hasher)
    if(not await DatabaseFriend.CheckDatabaseConnection()):
        raise DatabaseConnectionFailed()

@app.get("/") 
async def root():
    return {"message": "Hello World"}

@app.post("/authorization", response_model=SuccessAuthorizationResponseModel)
async def Authorization(Login: str, Password: str):
    Logger.Log(f"Authorization attempt with login - {Login}", 1)
    if(DatabaseFriend):
        try: 
            Authorized = await DatabaseFriend.\
                        CheckUserAuthorizationData(Login, Password)
        except DatabaseFriendCheckAuthorizationDataError:
            raise HTTPException(
                status_code=500, 
                detail="Verify user authorization data impossible. "\
                        "Database access error."
            )
        except DatabaseFriendUserNotFoundError:
            raise HTTPException(
                status_code=404, 
                detail="Verify user authorization data impossible. "\
                        "User not found."
            )
        else:
            if(Authorized):
                Logger.Log(f"User with login - {Login}, authorized", 2)
                return { 
                    "Token": Hasher.GetToken(Login, \
                                    Hasher.HashOfPassword(Password)) 
                }
            else:
                Logger.Log(f"Authorization denied for user with login {Login}"\
                                                " - wrong login or password", 3)
                raise HTTPException(
                    status_code=404, 
                    detail="Authorization data wrong. Check you login and password."
                )
    Logger.Log(f"Unusual turn of events during authorization", 2)
    raise HTTPException(status_code=500)