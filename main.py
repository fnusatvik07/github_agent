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
    print(f"🧮 Adding {a} + {b} = {result}")  # Added emoji for easier log tracking
    return {"a": a, "b": b, "result": result}

@app.post("/webhook")
async def github_webhook(request: Request):
    body = await request.body()
    data = json.loads(body)
    
    print("🎯 GitHub webhook received!")
    
    # Extract basic info
    repo_name = data.get('repository', {}).get('full_name', 'Unknown')
    branch = data.get('ref', '').split('/')[-1] if data.get('ref') else 'unknown'
    commits = data.get('commits', [])
    
    print(f"� Repository: {repo_name}")
    print(f"🌿 Branch: {branch}")
    print(f"📝 Commits: {len(commits)}")
    
    # Analyze all changes across all commits
    all_added = []
    all_modified = []
    all_removed = []
    
    for commit in commits:
        commit_id = commit.get('id', 'unknown')[:8]
        message = commit.get('message', 'No message')
        
        print(f"  🔄 {commit_id}: {message}")
        
        # Collect file changes
        added = commit.get('added', [])
        modified = commit.get('modified', [])
        removed = commit.get('removed', [])
        
        all_added.extend(added)
        all_modified.extend(modified) 
        all_removed.extend(removed)
        
        print(f"     ➕ Added: {added}")
        print(f"     🔄 Modified: {modified}")
        print(f"     ❌ Removed: {removed}")
    
    # Remove duplicates
    unique_added = list(set(all_added))
    unique_modified = list(set(all_modified))
    unique_removed = list(set(all_removed))
    
    print(f"\n📊 Summary of all changes:")
    print(f"  ➕ Total Added: {len(unique_added)} files - {unique_added}")
    print(f"  🔄 Total Modified: {len(unique_modified)} files - {unique_modified}")
    print(f"  ❌ Total Removed: {len(unique_removed)} files - {unique_removed}")
    
    # Check if README should be updated
    python_files_changed = [f for f in unique_added + unique_modified if f.endswith('.py')]
    readme_changed = any('readme' in f.lower() for f in unique_modified)
    
    print(f"\n🐍 Python files changed: {python_files_changed}")
    print(f"📖 README already updated: {readme_changed}")
    
    if python_files_changed and not readme_changed:
        print("🚨 ACTION NEEDED: Python files changed but README not updated!")
        print("💡 Should update README to reflect code changes")
    else:
        print("✅ No README update needed")
    
    return {
        "status": "success", 
        "message": "Change analysis complete",
        "analysis": {
            "repo": repo_name,
            "branch": branch, 
            "commits": len(commits),
            "files_added": unique_added,
            "files_modified": unique_modified,
            "files_removed": unique_removed,
            "python_files_changed": python_files_changed,
            "readme_needs_update": python_files_changed and not readme_changed
        }
    }

if __name__ == "__main__":
    print("Starting GitHub Agent...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
