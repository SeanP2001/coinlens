from fastapi import FastAPI

# creating app
app = FastAPI()

# defining api endpoint
@app.get("/")
def first_example():
    return {"message": "Hello, FastAPI!"}