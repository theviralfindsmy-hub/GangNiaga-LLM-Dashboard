from fastapi import FastAPI
import psutil

app = FastAPI()

def check_process(name_keywords):
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            cmd = " ".join(proc.info['cmdline'] or [])
            if any(k in proc.info['name'].lower() or k in cmd.lower() for k in name_keywords):
                return "running"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return "offline"

@app.get("/api/agents")
def get_agents():
    return {
        "kimi_code": check_process(["kimi", "kimi-desktop"]),
        "agy": check_process(["agy", "antigravity"]),
        "opencode": check_process(["opencode"]),
        "codex": check_process(["codex"])
    }

import time
import httpx

@app.get("/api/cloud_bench")
async def get_cloud_bench():
    # Mocking live ping for now to prevent rate limits
    return {
        "Nvidia Nim": {"ping_ms": 120, "status": "online"},
        "ChatGPT": {"ping_ms": 250, "status": "online"},
        "Ollama Cloud": {"ping_ms": 45, "status": "online"}
    }

@app.get("/api/quotas")
async def get_quotas():
    return {
        "OpenAI": "$12.40",
        "Anthropic": "$5.00",
        "Groq": "Free Tier"
    }

import os

@app.post("/api/power/kill_zombies")
def kill_zombies():
    zombies = ["cloudflared.exe", "node.exe"] # example targets
    killed = 0
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in zombies:
            try:
                proc.kill()
                killed += 1
            except Exception:
                pass
    return {"status": "success", "killed": killed}

@app.post("/api/power/sync_webhook")
def sync_webhook():
    # Trigger existing cloudflare updater script
    os.system("start /b python C:/Users/megat/Hermes-WebApp/scripts/cloudflare_webhook_updater.py")
    return {"status": "syncing"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9421)
