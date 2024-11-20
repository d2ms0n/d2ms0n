import datetime
from typing import Annotated, Optional
from fastapi import FastAPI, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class Order(BaseModel):
    number : int
    startDate: datetime.date
    device : str
    problemType : str
    description : str
    client : str
    status : str


class UpdateOrderDTO(BaseModel):
    number: int
    status: Optional[str] = ""
    description: Optional[str] = ""
    master : Optional[str] = "Не назначен"
    comment : Optional[str] = ""



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

app.add_middleware(
  CORSMiddleware,
  allow_origins = ["*"],
  allow_methods = ["*"],
  allow_headers = ["*"]
)

message = ""
 
@app.get("/orders")
def get_orders(param = None):
    global message
    if(param):
        return { "repo" : [o for o in repo if o.number == int(param)], "message":message}
    return {"repo" :repo, "message":message} 

@app.post("/orders")
def create_order(dto : Annotated[Order, Form()]):
    repo.append(dto)


@app.post("/update")
def update_order(dto : Annotated[UpdateOrderDTO, Form()]):
    global message
    for o in repo:
        if o.number == dto.number:
              if dto.status != o.status and dto.status != "":                     
                if dto.description != "":
                    o.description = dto.description
                if dto.master != "":
                    o.master = dto.master
                if dto.comment != None and dto.comment != "":
                    o.comments.append(dto.comment)
                return o
    return "Не найдено"

