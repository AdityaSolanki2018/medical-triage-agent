import anthropic

def check_symptom_severity(symptoms: str, age: int) -> dict:
    """
    Checks a list of symptoms and returns severity indicators.
    The agent calls this when it needs to assess how serious symptoms are.
    """
    emergency_keywords = [
        "chest pain", "difficulty breathing", "shortness of breath",
        "stroke", "unconscious", "severe bleeding", "heart attack",
        "can't breathe", "crushing pain", "sudden vision loss"
    ]

    high_risk_keywords = [
        "high fever", "severe headache", "vomiting blood",
        "severe abdominal pain", "confusion", "numbness"
    ]

    symptoms_lower = symptoms.lower()

    for keyword in emergency_keywords:
        if keyword in symptoms_lower:
            return {
                "severity": "emergency",
                "reason": f"Detected emergency symptom: '{keyword}'",
                "call_911": True
            }

    for keyword in high_risk_keywords:
        if keyword in symptoms_lower:
            return {
                "severity": "high",
                "reason": f"Detected high-risk symptom: '{keyword}'",
                "call_911": False
            }

    if age > 65 or age < 5:
        return {
            "severity": "medium",
            "reason": "Patient is in a higher-risk age group (elderly or infant)",
            "call_911": False
        }

    return {
        "severity": "low",
        "reason": "No immediately alarming symptoms detected",
        "call_911": False
    }


def check_drug_interaction(medications: str) -> dict:
    """
    Simulates checking for drug interactions.
    In a real app this would call a medical API like RxNorm or OpenFDA.
    """
    known_interactions = {
        ("warfarin", "aspirin"): "HIGH RISK: Increases bleeding risk significantly",
        ("ssri", "maoi"): "DANGEROUS: Can cause serotonin syndrome",
        ("metformin", "alcohol"): "WARNING: Risk of lactic acidosis",
    }

    medications_lower = medications.lower()
    found_interactions = []

    for (drug1, drug2), warning in known_interactions.items():
        if drug1 in medications_lower and drug2 in medications_lower:
            found_interactions.append(warning)

    if found_interactions:
        return {"interactions_found": True, "warnings": found_interactions}

    return {"interactions_found": False, "warnings": []}


# This is the schema we pass to Claude so it KNOWS what tools exist
# and what arguments each tool needs. Think of it as a job description
# for each tool.
TOOLS = [
    {
        "name": "check_symptom_severity",
        "description": "Analyzes patient symptoms and age to determine severity level. Use this first when a patient describes their symptoms.",
        "input_schema": {
            "type": "object",
            "properties": {
                "symptoms": {
                    "type": "string",
                    "description": "The symptoms described by the patient"
                },
                "age": {
                    "type": "integer",
                    "description": "The age of the patient"
                }
            },
            "required": ["symptoms", "age"]
        }
    },
    {
        "name": "check_drug_interaction",
        "description": "Checks if there are dangerous interactions between medications the patient is taking. Use this if the patient mentions any medications.",
        "input_schema": {
            "type": "object",
            "properties": {
                "medications": {
                    "type": "string",
                    "description": "Comma-separated list of medications the patient is taking"
                }
            },
            "required": ["medications"]
        }
    }
]