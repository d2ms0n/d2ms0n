import datetime 
from typing import Annotated, Optional, Union
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi import Cookie, FastAPI, Form, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4

class Order(BaseModel):
    number : int
    startDate: datetime.date
    device : str
    problemType : str
    description : str
    client : str
    status : str
    endDate: Optional[datetime.date] = None
    master : Optional[str] = "Не назначен"
    comments : Optional[list] = []

class UpdateOrderDTO(BaseModel):
    number: int
    status: Optional[str] = ""
    description: Optional[str] = ""
    master: Optional[str] = ""
    comment : Optional[str] = str

Users = {"admin":"admin", "user":"user"}
Tokens = {}

repo = [
    Order(
        number = 1,
        startDate = "2000-12-01",
        device = "123",
        problemType = "123",
        description = "123",
        client = "123",
        status = "в ожидании"
    ),
    Order(
        number = 2,
        startDate = "2000-12-01",
        device = "123",
        problemType = "123",
        description = "123",
        client = "123",
        status = "в ожидании"
    ),
    Order(
        number = 3,
        startDate = "2000-12-01",
        device = "123",
        problemType = "123",
        description = "123",
        client = "123",
        status = "в ожидании"
    )
]


app = FastAPI()

app.mount("/static", StaticFiles(directory="public", html=True))
 
app.add_middleware(
  CORSMiddleware,
  allow_origins = ["*"],
  allow_methods = ["*"],
  allow_headers = ["*"]
)

message = ""

def isauto(request):
    login = request.cookies.get('login')
    token = request.cookies.get('token') 
    if login in Tokens: 
        val =  Tokens[login] 
        if val== token:
            return True

    return False







@app.get("/orders")
def get_orders(request: Request, param = None):
    if not isauto(request): 
       return "noauth"
    global message
    buffer = message
    message=""
    if(param):
        return { "repo" : [o for o in repo if o.number == int(param)], "message": buffer}
    return {"repo" :repo, "message": buffer}

@app.post("/orders")
def create_order(dto : Annotated[Order, Form()], request: Request):
    if not isauto(request): 
        return "noauth"
        
    repo.append(dto)

@app.post("/update")
def update_order(dto : Annotated[UpdateOrderDTO, Form()], request: Request):
    if not isauto(request): 
        return RedirectResponse("/static/auth.html") 
       
    global message
    for o in repo:
        if o.number == dto.number:
            if dto.status != o.status and dto.status != "":
                o.status = dto.status
                message += f"Статус заявки №{o.number} изменен\n"
                if(o.status == "выполнено"):
                    message += f"Заявка №{o.number} завершена\n"
                    o.endDate = datetime.datetime.now()
            if dto.description != "":
                o.description = dto.description
            if dto.master != "":
                o.master = dto.master
            if dto.comment != None and dto.comment != "":
                o.comments.append(dto.comment)
            return o
    return "Не найдено"

def complete_count():
    return len([o for o in repo if o.status == "выполнено"])

def get_problem_type_stat():
    dict = {}
    for o in repo:
        if o.problemType in dict.keys():
            dict[o.problemType] += 1
        else:
            dict[o.problemType] = 1
    return dict

def get_average_time_to_complete():
    times = [(
        datetime.datetime.fromisoformat(o.endDate.isoformat()) -
        datetime.datetime.fromisoformat(o.startDate.isoformat())).days 
                 for o in repo 
                 if o.status == "выполнено"]
    if complete_count() != 0:
        return sum(times) / complete_count()
    return 0
    
@app.get("/statistics")
def get_statistics(request: Request):
    if not isauto(request): 
        return "noauth"
    
    return {"complete_count" : complete_count(),
        "problem_type_stat" : get_problem_type_stat(),
        "average_time_to_complete" : get_average_time_to_complete()}

@app.get("/auth")
def get_orders(login = None, password  = None):



    if login in Users and password == Users[login]: 
        token = uuid4()
        Tokens[login] = str(token)
        return token


    
    

@app.get("/")
def go_index(request: Request):
    if not isauto(request): 
        return RedirectResponse("/static/auth.html")
    
    return RedirectResponse("/static/stat.html")
          




    