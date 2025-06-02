from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from new import Task
import shutil
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Сервер начал работу')
    path = os.path.join(os.path.dirname(__file__), 'img')
    if not os.path.exists(path):
        os.mkdir(path)
    yield
    if os.path.exists(path):
        shutil.rmtree(path)
    print('Сервер закончил работу')


class Answers(BaseModel):
    q1: str
    q2: str
    q3: str


class User(BaseModel):
    name: str
    group: str
    answers: Answers | None = None
    results: dict[str, bool] | None = None


db_tasks = {}
db_users = {}

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # Разрешить передачу cookies
    allow_methods=["*"],       # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],       # Разрешить все заголовки
)

@app.post("/generate-task")
async def generate_task(user: User):
    task = Task()
    db_tasks[task.id] = task
    db_users[task.id] = user
    task.draw_graph()
    return {"imageId": task.id}

@app.get("/img/{id}")
async def get_img(id: str):
    return FileResponse(db_tasks[id].path, media_type="image/png")

@app.get("/task/{id}")
async def get_task(id: str):
    print(db_tasks[id])
    return dict(zip(["y_2", "start_x_3", "end_x_3", "correct_more"], db_tasks[id].get_question_data()))

@app.post("/answers/{id}")
async def check_answers(id: str, answers: Answers):
    print(answers.q1, answers.q2, answers.q3)
    db_users[id].answers = answers
    db_users[id].results = dict(zip(["result_1", "result_2", "result_3"], \
                                    db_tasks[id].check_answers(db_users[id].answers.q1, \
                                                               db_users[id].answers.q2, \
                                                               db_users[id].answers.q3)))
    print(db_users[id].results)


@app.get("/result/{id}")
async def send_results(id: str):
    return db_users[id].results | dict([['name', db_users[id].name], ["group", db_users[id].group], \
                                        ['start', db_tasks[id].time_start.strftime("%H:%M:%S")], ['finish', db_tasks[id].time_finish.strftime("%H:%M:%S")], \
                                        ['solving', db_tasks[id].time_solving]])
