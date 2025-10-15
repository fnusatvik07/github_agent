from fastapi import FastAPI, Request
import uvicorn
import json

app = FastAPI()

@app.get("/")
def health():
    # Health check endpoint
    return {"status": "healthy", "message": "API is running!"}

@app.post("/add")
def add_numbers(a: int, b: int):
    result = a + b
    print(f"Adding {a} + {b} = {result}")  # Added logging
    return {"a": a, "b": b, "result": result}

@app.post("/webhook")
async def github_webhook(request: Request):
    body = await request.body()
    data = json.loads(body)
    
    print("🎯 GitHub webhook received!")
    print("📄 Raw GitHub data:")
    print("=" * 50)
    print(json.dumps(data, indent=2))
    print("=" * 50)
    
    return {"status": "success", "message": "Raw data logged"}

if __name__ == "__main__":
    print("Starting GitHub Agent...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
