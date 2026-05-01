# 🏥 AI Medical Triage Agent

An agentic AI system that triages patient symptoms using LLM tool-calling, FastAPI, and Docker. Built with the ReAct (Reasoning + Acting) pattern.

## 🎯 What it does

A patient describes their symptoms → the AI agent autonomously:
1. Calls a symptom severity checker tool
2. Calls a drug interaction checker tool (if medications mentioned)
3. Reasons over the results
4. Returns a structured triage assessment with urgency level

## 🏗️ Architecture

User Request → FastAPI → Agentic Loop → Tool Calling → Structured Response
↓
[check_symptom_severity]
[check_drug_interaction]

## 🛠️ Tech Stack

- **LLM**: GPT-4o via OpenAI API
- **Agentic Pattern**: ReAct loop with tool-calling
- **API Framework**: FastAPI + Pydantic
- **Containerization**: Docker
- **Cloud**: Azure App Service
- **Language**: Python 3.11

## 🚀 Run Locally

### Prerequisites
- Python 3.11+
- Docker Desktop
- OpenAI API key

### Without Docker

```bash
git clone https://github.com/YOUR_USERNAME/medical-triage-agent.git
cd medical-triage-agent
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
echo "OPENAI_API_KEY=your_key_here" > .env
uvicorn main:app --reload
```

### With Docker

```bash
docker build -t medical-triage-agent .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here medical-triage-agent
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Service status |
| POST | `/triage` | Run triage agent |

### Example Request

```json
POST /triage
{
  "patient_name": "John Smith",
  "age": 45,
  "symptoms": "severe chest pain and difficulty breathing",
  "duration_hours": 2,
  "existing_conditions": "hypertension"
}
```

### Example Response

```json
{
  "patient_name": "John Smith",
  "urgency_level": "emergency",
  "assessment": "...",
  "recommended_action": "...",
  "follow_up_questions": ["..."],
  "disclaimer": "This is AI-generated guidance only. Always consult a real doctor."
}
```

## 🧠 Key Concepts Demonstrated

- **Agentic AI**: LLM autonomously decides which tools to call and in what order
- **Tool Calling**: Structured function calling with JSON schema validation
- **ReAct Pattern**: Reasoning and Acting in an iterative loop
- **Pydantic Models**: Strict input/output validation
- **REST API Design**: Clean endpoint structure with proper error handling
- **Containerization**: Reproducible deployment with Docker

## ⚠️ Disclaimer

This is a portfolio/demonstration project. Not intended for real medical use.