from fastapi import FastAPI, Request
import uvicorn
import json

app = FastAPI()

@app.get("/")
def health():
    return {"status": "healthy", "message": "API is running!"}

@app.post("/add")
def add_numbers(a: int, b: int):
    result = a + b
    return {"a": a, "b": b, "result": result}

@app.post("/webhook")
async def github_webhook(request: Request):
    body = await request.body()
    data = json.loads(body)
    
    print("🎯 GitHub webhook received!")
    print(f"Repository: {data.get('repository', {}).get('full_name', 'Unknown')}")
    
    return {"status": "success", "message": "Webhook received"}

if __name__ == "__main__":
    print("Starting GitHub Agent...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
