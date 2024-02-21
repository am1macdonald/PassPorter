from fastapi import FastAPI, Request

def signup(request: Request):
    print(request)

