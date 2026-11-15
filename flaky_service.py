import random

def call_service():
    if random.random() < 0.3:
        raise ConnectionError("Service Error")
    else:
        return "ok"