from fastapi import FastAPI


blogAPI = FastAPI()


@blogAPI.get('/')
async def hello():
    return {'Hello': 'world'}
