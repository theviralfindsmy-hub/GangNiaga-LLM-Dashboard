# Universal LLM Dashboard - Aggregator Daemon Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python FastAPI background daemon that fetches CLI agent statuses, quotas, and cloud latencies, exposing them as a JSON REST API for the Rust frontend.

**Architecture:** A lightweight FastAPI server running on port 9421. It uses `psutil` to scan for agent processes, standard `httpx` to ping cloud endpoints, and subprocess to trigger system healing commands.

**Tech Stack:** Python 3.12+, FastAPI, Uvicorn, psutil, httpx.

## Global Constraints

- Must run as a background daemon without blocking the UI.
- Use port 9421 for the REST API.
- All endpoints must return standard JSON.

---

### Task 1: Setup FastAPI Server and Process Scanner

**Files:**
- Create: `C:\Users\megat\llmfit-repo\llmfit-aggregator\main.py`
- Create: `C:\Users\megat\llmfit-repo\llmfit-aggregator\requirements.txt`

**Interfaces:**
- Produces: REST endpoint `GET /api/agents` returning `{ "kimi_code": "running", "agy": "offline", "opencode": "running" }`

- [ ] **Step 1: Write requirements and basic server**

```python
# C:\Users\megat\llmfit-repo\llmfit-aggregator\requirements.txt
fastapi
uvicorn
psutil
httpx
```

```python
# C:\Users\megat\llmfit-repo\llmfit-aggregator\main.py
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9421)
```

- [ ] **Step 2: Run test to verify it works**

Run: `uv run uvicorn main:app --port 9421 & curl http://127.0.0.1:9421/api/agents`
Expected: Returns JSON with agent statuses.

- [ ] **Step 3: Commit**

```bash
git add llmfit-aggregator/
git commit -m "feat: add aggregator process scanner"
```

### Task 2: Cloud Benchmark & Quota Endpoints

**Files:**
- Modify: `C:\Users\megat\llmfit-repo\llmfit-aggregator\main.py`

**Interfaces:**
- Produces: REST endpoints `GET /api/cloud_bench` and `GET /api/quotas`

- [ ] **Step 1: Write endpoints in main.py**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add llmfit-aggregator/main.py
git commit -m "feat: add mock cloud bench and quota endpoints"
```

### Task 3: Power Tools Endpoints (Auto-Heal & Sync)

**Files:**
- Modify: `C:\Users\megat\llmfit-repo\llmfit-aggregator\main.py`

**Interfaces:**
- Produces: `POST /api/power/kill_zombies` and `POST /api/power/sync_webhook`

- [ ] **Step 1: Write endpoints in main.py**

```python
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
```

- [ ] **Step 2: Commit**

```bash
git add llmfit-aggregator/main.py
git commit -m "feat: add power tools execution endpoints"
```
