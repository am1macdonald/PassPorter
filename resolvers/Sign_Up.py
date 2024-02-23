from fastapi import FastAPI, Request


class SignupResolver:
    def __init__(self, request: Request):
        self.request = request
        print(request)
