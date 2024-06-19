from fastapi import FastAPI

from .schemas import Message

app = FastAPI()


@app.get('/', response_model=Message)
def read_root():
    return {'mensagem': 'Olá mundo!'}
