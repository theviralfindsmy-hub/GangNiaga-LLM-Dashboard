# Universal LLM Dashboard - Rust TUI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Modify `llmfit-tui` to include top navigation tabs and fetch data from the Aggregator daemon.

**Architecture:** Extend Ratatui state with `DashboardMode`. HTTP client (`ureq` or `reqwest`) fetches JSON from port 9421.

**Tech Stack:** Rust (Edition 2024), ratatui, ureq, serde_json.

## Global Constraints

- Must not block the main UI render loop when fetching HTTP data (use async or separate thread).
- Retain existing `Local Fit` functionality exactly as it is.

---

### Task 1: Add Dashboard Mode to State

**Files:**
- Modify: `C:\Users\megat\llmfit-repo\llmfit-tui\src\tui_app.rs`

**Interfaces:**
- Produces: `enum AppTab { LocalFit, Agents, CloudBench, PowerTools }`

- [ ] **Step 1: Add AppTab enum and update App struct**

```rust
// In tui_app.rs
#[derive(PartialEq)]
pub enum AppTab {
    LocalFit,
    Agents,
    CloudBench,
    PowerTools,
}

// Inside `pub struct App`
// Add field: pub active_tab: AppTab,
```

- [ ] **Step 2: Commit**

```bash
git add llmfit-tui/src/tui_app.rs
git commit -m "feat: add AppTab enum to TUI state"
```

### Task 2: Render Top Navigation Bar

**Files:**
- Modify: `C:\Users\megat\llmfit-repo\llmfit-tui\src\tui_ui.rs`

**Interfaces:**
- Consumes: `AppTab` from `tui_app.rs`

- [ ] **Step 1: Render tabs at the top of the UI**

```rust
// In tui_ui.rs, inside the main draw function, allocate a chunk for tabs.
// Use `ratatui::widgets::Tabs` to display [F1] Local Fit, [F2] Agents, [F3] Cloud Bench, [F4] Power Tools.
```

- [ ] **Step 2: Commit**

```bash
git add llmfit-tui/src/tui_ui.rs
git commit -m "feat: render top navigation tabs"
```

### Task 3: Handle Key Events for Navigation

**Files:**
- Modify: `C:\Users\megat\llmfit-repo\llmfit-tui\src\tui_events.rs`

**Interfaces:**
- Consumes: `AppTab`

- [ ] **Step 1: Map F1-F4 keys to change tabs**

```rust
// In tui_events.rs
// On KeyCode::F(1) -> app.active_tab = AppTab::LocalFit;
// On KeyCode::F(2) -> app.active_tab = AppTab::Agents;
// On KeyCode::F(3) -> app.active_tab = AppTab::CloudBench;
// On KeyCode::F(4) -> app.active_tab = AppTab::PowerTools;
```

- [ ] **Step 2: Commit**

```bash
git add llmfit-tui/src/tui_events.rs
git commit -m "feat: map F1-F4 keys to tab navigation"
```

### Task 4: Fetch and Display Aggregator Data

**Files:**
- Modify: `C:\Users\megat\llmfit-repo\llmfit-tui\Cargo.toml`
- Modify: `C:\Users\megat\llmfit-repo\llmfit-tui\src\tui_ui.rs`

- [ ] **Step 1: Add HTTP fetch logic (Mocked for UI first)**

```rust
// Fetch JSON from `http://127.0.0.1:9421/api/agents` and render it when `AppTab::Agents` is active.
```

- [ ] **Step 2: Commit**

```bash
git add llmfit-tui/
git commit -m "feat: render agent and cloud bench data"
```
