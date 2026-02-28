"""FastAPI app with CORS enabled."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents import PatientAgent

app = FastAPI(title="HealthSync API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

patient_agent = PatientAgent()


class ShareRecordsRequest(BaseModel):
    query: str
    context: str | None = None


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/agent/share-records")
def share_records(body: ShareRecordsRequest):
    """Ask the patient agent to share medical record information."""
    return {
        "response": patient_agent.share_records(
            query=body.query, context=body.context
        )
    }


# Demo: sample medical context for hospital request simulation
DEMO_CONTEXT = """
Patient: Jane Doe, DOB 1985-03-12
Allergies: Penicillin
Conditions: Type 2 diabetes (controlled), hypertension
Medications: Metformin 500mg BID, Lisinopril 10mg daily
Last visit: 2024-01-15 - Annual checkup, A1C 6.2%
Labs (recent): Fasting glucose 108, BP 128/82
"""


# Canned demo response when ANTHROPIC_API_KEY is not set or LLM call fails
DEMO_QUERY = "We need relevant medical history and current medications for emergency department intake."
DEMO_THINKING = [
    "Request is from hospital for ED intake — appropriate to share.",
    "Identifying: allergies (critical), conditions, current meds, recent labs.",
    "Excluding non-essential details; keeping data minimal and relevant.",
]
DEMO_AGENT_RESPONSE = (
    "For ED intake, here is the relevant information from the patient record:\n\n"
    "**Allergies:** Penicillin\n\n"
    "**Conditions:** Type 2 diabetes (controlled), hypertension\n\n"
    "**Current medications:** Metformin 500mg twice daily, Lisinopril 10mg daily\n\n"
    "**Recent labs:** Fasting glucose 108 mg/dL, BP 128/82 (from last visit).\n\n"
    "Last annual checkup was 2024-01-15 with A1C 6.2%."
)
DEMO_RECORDS_SHARED = [
    "Allergies: Penicillin",
    "Conditions: Type 2 diabetes (controlled), hypertension",
    "Current medications: Metformin 500mg BID, Lisinopril 10mg daily",
    "Recent labs: Fasting glucose 108, BP 128/82",
]


@app.post("/demo")
def demo():
    """Simulate a hospital request: agent decides what to share and returns thinking + conversation + records."""
    query = DEMO_QUERY
    thinking = DEMO_THINKING.copy()
    records_shared = DEMO_RECORDS_SHARED.copy()

    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            response = patient_agent.share_records(query=query, context=DEMO_CONTEXT)
        except Exception:
            response = DEMO_AGENT_RESPONSE
    else:
        response = DEMO_AGENT_RESPONSE

    conversation = [
        {"role": "user", "content": query},
        {"role": "agent", "content": response},
    ]
    return {
        "thinking": thinking,
        "conversation": conversation,
        "records_shared": records_shared,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
