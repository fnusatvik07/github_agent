from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def health():
    return {"status": "healthy", "message": "API is running!"}

@app.post("/add")
def add_numbers(a: int, b: int):
    result = a + b
    return {"a": a, "b": b, "result": result}

if __name__ == "__main__":
    print("Starting GitHub Agent...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
