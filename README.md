# 🔧 Workflow Builder — Conversational AI Automation Agent

> **Describe your automation in plain English. The AI asks the right questions, then renders a live blueprint workflow diagram — instantly.**

<video src="./workflow_builder_DEMO.mp4" controls width="100%"></video>

> 📽️ **[▶ Watch Demo Video](./workflow_builder_DEMO.mp4)** — See the full conversational flow from plain-English description to live workflow canvas.

---

## 🌐 Live Demo

> **Try it now — running 24/7 on Azure Cloud:**

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Azure%20Cloud-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://ca-frontend.kindrock-91ecbb54.southindia.azurecontainerapps.io/)

**[https://ca-frontend.kindrock-91ecbb54.southindia.azurecontainerapps.io/](https://ca-frontend.kindrock-91ecbb54.southindia.azurecontainerapps.io/)**

Deployed on **Azure Container Apps** (South India region) — no setup needed, open the link and start building workflows instantly.

---

## ✨ What It Does

**Workflow Builder** is a conversational AI agent that turns natural language into visual workflow automation diagrams. Instead of drag-and-drop complexity, you just describe what you want to automate in chat. The AI asks targeted clarification questions to fill in the exact parameters it needs, then generates a structured, interactive node-graph blueprint on the canvas — ready to export or hand off to your automation platform.

### Key Features

- 🤖 **Conversational Clarification** — LangGraph-powered multi-turn agent extracts trigger, condition, action, destination, and notification fields through natural dialogue
- 🎨 **Live Blueprint Canvas** — React Flow renders an interactive, auto-layouted workflow diagram the moment all fields are collected
- ✅ **Information Checklist** — Real-time progress tracker shows which fields have been confirmed vs. pending in every AI reply
- 🔍 **Smart Validation** — The agent refuses vague or non-sensical answers (e.g. "my pocket" as a trigger source) and re-asks with helpful context
- 🔁 **Session Reset** — Start a fresh workflow any time with one click
- 🐳 **Docker Ready** — Full `docker-compose` setup for both services
- ☁️ **Azure Cloud Deployed** — CI/CD via GitHub Actions → Azure Container Registry → Azure Container Apps

---

## 🏗️ Architecture

### 1. LangGraph Agent — Graph Flow

```mermaid
flowchart TD
    START(["⬛ START"])
    UI(["👤 User Message"])
    A["🧠 understand_intent\nExtract fields from first message\nvia structured LLM call"]
    B["🔍 extract_info\nCheck which of the 7 required\nfields are still missing"]
    C{"Missing\nfields?"}
    D["❓ ask_clarification\nGenerate targeted question\nfor next missing field"]
    E["✅ process_clarification_response\nValidate user answer;\nset uncertainty_flag if vague"]
    F{"Answer\nuncertain?"}
    G["🗺️ generate_workflow\nAssemble node/edge JSON\nfor React Flow canvas"]
    END(["🏁 END\n→ Return workflow JSON"])

    START --> UI --> A
    A --> B
    B --> C
    C -- "fields missing" --> D
    C -- "all fields collected" --> G
    D -- "interrupt: wait for user reply" --> E
    E --> F
    F -- "yes: re-ask" --> D
    F -- "no: re-check" --> B
    G --> END

    style START fill:#1e1e2e,color:#cdd6f4,stroke:#45475a
    style END fill:#1e1e2e,color:#a6e3a1,stroke:#45475a
    style D fill:#313244,color:#cba6f7,stroke:#cba6f7
    style E fill:#313244,color:#f38ba8,stroke:#f38ba8
    style G fill:#313244,color:#a6e3a1,stroke:#a6e3a1
    style A fill:#313244,color:#89b4fa,stroke:#89b4fa
    style B fill:#313244,color:#89dceb,stroke:#89dceb
```

---

### 2. Full System + Deployment Architecture

```
 ╔══════════════════════════════════════════════════════════════════╗
 ║              GitHub Actions CI/CD Pipeline                       ║
 ║  push → main                                                     ║
 ║    ├─ docker build  Dockerfile.backend  → workflow-backend:sha   ║
 ║    ├─ docker build  Dockerfile.frontend → workflow-frontend:sha  ║
 ║    ├─ docker push   → Azure Container Registry (ACR)            ║
 ║    ├─ az containerapp update → ca-backend  (port 8000)           ║
 ║    └─ az containerapp update → ca-frontend (port 80)            ║
 ╚══════════════════════════════════════════════════════════════════╝
                               │
              ┌────────────────┴─────────────────┐
              ▼                                   ▼
 ┌─────────────────────────┐       ┌──────────────────────────────┐
 │  Azure Container App    │       │  Azure Container App         │
 │  ca-frontend (nginx)    │       │  ca-backend  (FastAPI)       │
 │  ─────────────────────  │       │  ────────────────────────    │
 │  React 19 + Vite        │       │  Python 3.12 + uvicorn       │
 │  ┌─────────────────┐    │  REST │  ┌────────────────────────┐  │
 │  │  Chat Panel     │    │──────▶│  │  LangGraph Agent Graph │  │
 │  │  - History      │    │POST   │  │  ─────────────────────  │  │
 │  │  - Checklist    │    │/api/  │  │  understand_intent      │  │
 │  │  - Reset btn    │    │chat   │  │  extract_info           │  │
 │  └─────────────────┘    │       │  │  ask_clarification      │  │
 │  ┌─────────────────┐    │◀──────│  │  process_clarification  │  │
 │  │ Workflow Canvas  │    │JSON   │  │  generate_workflow      │  │
 │  │ React Flow      │    │resp.  │  └────────────────────────┘  │
 │  │ dagre layout    │    │       │  MemorySaver (per thread_id) │
 │  └─────────────────┘    │       │  OpenRouter → Gemini 2.5    │
 └─────────────────────────┘       └──────────────────────────────┘
              │                                   │
              └────────────────┬─────────────────┘
                               ▼
                  Azure Container Apps Environment
                  (South India region · 24/7 uptime)
```

### Agent Graph Nodes

| Node | Role |
|---|---|
| `understand_intent` | Extracts structured fields from the user's first message using a structured-output LLM call |
| `extract_info` | Checks which of the 7 required fields are still missing |
| `ask_clarification` | Generates a targeted, context-aware question for the next missing field |
| `process_clarification_response` | Validates the user's answer; sets `uncertainty_flag` if vague/invalid |
| `generate_workflow` | Deterministically assembles the node/edge JSON for the canvas |

### Workflow Fields Collected

| Field | Example |
|---|---|
| `trigger_source` | Google Sheets, Gmail, Slack |
| `trigger_event` | New row added, file uploaded |
| `condition` | Amount > 500, status = "urgent" |
| `action` | Send a message, log event |
| `destination` | Google Sheets, Notion, database |
| `notification_channel` | Slack, Telegram, email |
| `duplicate_handling` | yes / no |

---

## 🛠️ Tech Stack

### Backend
- **Python 3.12+** with `uv` for dependency management
- **FastAPI** — REST API with CORS middleware
- **LangGraph** — Stateful multi-node agent graph with `MemorySaver` checkpointing
- **LangChain / LangChain-OpenAI** — LLM interface with structured output (Pydantic)
- **OpenRouter** — LLM gateway (model: `google/gemini-2.5-flash-lite`)
- **LangSmith** — Optional tracing & observability

### Frontend
- **React 19** with **Vite 8**
- **@xyflow/react** (React Flow) — Interactive node-graph canvas
- **@dagrejs/dagre** — Automatic left-to-right graph layout
- **Tailwind CSS v4** — Utility-first styling
- **lucide-react** — Icon library

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- `uv` (Python package manager) — `pip install uv`

### 1. Clone & Set Up Environment

```bash
git clone <your-repo-url>
cd wrkflow-builder
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openrouter_api_key
OPENAI_BASE_URL=https://openrouter.ai/api/v1

# Optional: LangSmith tracing
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_key
LANGSMITH_PROJECT=workflow-builder
```

> **Note:** The backend uses OpenRouter as the LLM provider. Get a free API key at [openrouter.ai](https://openrouter.ai).

### 2. Start the Backend

```bash
# Create virtual environment and install dependencies
uv venv
uv sync

# Activate (Windows)
.venv\Scripts\activate

# Start FastAPI server
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`. Check `http://localhost:8000/api/health` to confirm it's running.

### 3. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will open at `http://localhost:5173`.

---

## 🐳 Docker Compose

Run everything with a single command:

```bash
docker-compose up --build
```

This starts:
- **Backend** on port `8000`
- **Frontend** (nginx) on port `80`

Make sure your `.env` file is present in the project root before running.

---

## 🧪 CLI Testing (No Frontend)

You can test the full agent loop from the terminal:

```bash
python main.py
```

This runs an interactive CLI session that walks through the same clarification loop and prints the final workflow JSON.

You can also run the API test script:

```bash
cd frontend
python test_api.py
```

---

## 📁 Project Structure

```
wrkflow-builder/
├── server.py               # FastAPI app + /api/chat endpoint
├── main.py                 # CLI test harness
├── configs.py              # Model & project config
├── requirements.txt        # Pinned Python deps
├── pyproject.toml          # uv project config
├── docker-compose.yml      # Multi-service Docker setup
├── Dockerfile.backend      # Backend image
│
├── graphs/
│   ├── builder.py          # LangGraph StateGraph assembly
│   ├── edges.py            # Conditional edge routing logic
│   └── state_schema.py     # WorkflowState TypedDict
│
├── nodes/
│   ├── understand_intent.py       # First-pass intent + field extraction
│   ├── extract_info.py            # Missing field checker
│   ├── ask_clarification.py       # Targeted question generator
│   ├── process_clarification.py   # Answer validator
│   └── generate_workflow.py       # Node/edge JSON assembler
│
└── frontend/
    ├── src/
    │   ├── App.jsx                 # Root state + API calls
    │   ├── services/api.js         # fetch() wrappers
    │   ├── components/
    │   │   ├── Layout/AppLayout.jsx
    │   │   ├── Chat/
    │   │   │   ├── ChatPanel.jsx
    │   │   │   ├── Message.jsx
    │   │   │   └── ChatInput.jsx
    │   │   └── Workflow/
    │   │       ├── WorkflowCanvas.jsx   # React Flow + Blueprint bg
    │   │       └── WorkflowNode.jsx     # Custom node renderer
    │   └── utils/
    │       ├── workflowLayout.js        # Dagre auto-layout
    │       └── iconMap.js              # Service → icon mapping
    └── vite.config.js
```

---

## 🔌 API Reference

### `POST /api/chat`

Send a user message and get the agent's response.

**Request body:**
```json
{
  "message": "Notify me on Slack when a new Stripe payment comes in",
  "thread_id": "session_abc123"
}
```

**Response:**
```json
{
  "message": "Which Slack channel should receive the payment notification?",
  "status": "needs_clarification",
  "workflow": null,
  "extracted_info": {
    "trigger_source": "Stripe",
    "trigger_event": "new payment",
    "notification_channel": "Slack"
  },
  "missing_fields": ["condition", "action", "destination", "duplicate_handling"],
  "thread_id": "session_abc123"
}
```

`status` is either `"needs_clarification"` or `"complete"`. When `"complete"`, the `workflow` field contains the full node/edge graph JSON.

### `POST /api/reset`

Reset a session's thread state.

### `GET /api/health`

Health check. Returns `{ "status": "ok", "model": "..." }`.

---

## 📄 License

MIT — feel free to use, fork, and extend.
