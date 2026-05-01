import os
from openai import OpenAI
from dotenv import load_dotenv
from app.tools import TOOLS, check_symptom_severity, check_drug_interaction
from app.models import SymptomInput, TriageResult, UrgencyLevel

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a medical triage assistant AI. Your job is to:
1. Analyze patient symptoms carefully
2. Use the available tools to assess severity
3. Ask follow-up questions if needed
4. Provide a structured triage assessment

Always use the check_symptom_severity tool first.
If the patient mentions medications, use the check_drug_interaction tool.
Be empathetic but clear. Always remind patients this is AI guidance, not a diagnosis.
"""

def run_triage_agent(patient_input: SymptomInput) -> TriageResult:
    """
    The main agentic loop — same logic, OpenAI client.
    """

    user_message = f"""
    Patient: {patient_input.patient_name}, Age: {patient_input.age}
    Symptoms: {patient_input.symptoms}
    Duration: {patient_input.duration_hours or 'Not specified'} hours
    Existing conditions: {patient_input.existing_conditions or 'None reported'}
    """

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    # Convert Anthropic-style tool schema to OpenAI-style
    openai_tools = [
        {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["input_schema"]
            }
        }
        for tool in TOOLS
    ]

    print(f"\n--- Starting triage for {patient_input.patient_name} ---")

    import json

    # ── THE AGENTIC LOOP ──
    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=openai_tools,
            tool_choice="auto"
        )

        message = response.choices[0].message
        stop_reason = response.choices[0].finish_reason

        print(f"Agent stop reason: {stop_reason}")

        # Agent wants to call a tool
        if stop_reason == "tool_calls":
            messages.append(message)  # Add agent's decision to history

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_input = json.loads(tool_call.function.arguments)

                print(f"Agent calling tool: {tool_name} with input: {tool_input}")

                if tool_name == "check_symptom_severity":
                    result = check_symptom_severity(**tool_input)
                elif tool_name == "check_drug_interaction":
                    result = check_drug_interaction(**tool_input)
                else:
                    result = {"error": "Unknown tool"}

                # Send tool result back to agent
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })

        # Agent is done reasoning
        elif stop_reason == "stop":
            final_text = message.content
            print("Agent final response received.")

            urgency = UrgencyLevel.LOW
            final_lower = final_text.lower()
            if "emergency" in final_lower:
                urgency = UrgencyLevel.EMERGENCY
            elif "high" in final_lower:
                urgency = UrgencyLevel.HIGH
            elif "medium" in final_lower or "moderate" in final_lower:
                urgency = UrgencyLevel.MEDIUM

            return TriageResult(
                patient_name=patient_input.patient_name,
                urgency_level=urgency,
                assessment=final_text,
                recommended_action="Please follow the assessment above. Call 911 if symptoms worsen suddenly.",
                follow_up_questions=[
                    "Have your symptoms gotten worse in the last hour?",
                    "Do you have anyone with you right now?",
                    "Are you able to keep fluids down?"
                ]
            )