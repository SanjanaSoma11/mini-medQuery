from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import math


app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "http://localhost:3000",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Load patient data
with open('mock_patient_data.json', 'r') as f:
    patient_data = json.load(f)

load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyC-9l-i7MMTBu1K-KgmY3_y46CHUrHQNeE"))
model = genai.GenerativeModel("gemini-2.0-flash")

def answer_question_without_llm(question):
    """Answer questions without LLM using direct data lookup"""
    question = question.lower()
    
    # Medication queries
    if 'medication' in question or 'taking' in question:
        meds = patient_data['medications']
        return {
            "answer": f"You are currently taking {len(meds)} medications: " + 
                     ", ".join([f"{m['name']} ({m['dosage']}, {m['frequency']})" for m in meds]),
            "data": meds,
            "confidence": 0.9
        }
    
    # Test result queries
    elif 'blood test' in question or 'last test' in question:
        last_test = sorted(patient_data['test_results'], key=lambda x: x['date'], reverse=True)[0]
        return {
            "answer": f"Your last blood test was on {last_test['date']} with results: {last_test['type']} = {last_test['value']}",
            "data": last_test,
            "confidence": 0.85
        }
    
    # Cholesterol queries
    elif 'cholesterol' in question:
        cholesterol_tests = [t for t in patient_data['test_results'] if t['type'].lower() == 'cholesterol']
        if cholesterol_tests:
            latest = sorted(cholesterol_tests, key=lambda x: x['date'], reverse=True)[0]
            return {
                "answer": f"Your latest cholesterol reading was {latest['value']} on {latest['date']}",
                "data": latest,
                "confidence": 0.9
            }
    
    # Visit queries
    elif 'cardiologist' in question or 'follow up' in question:
        cardio_visits = [v for v in patient_data['visits'] if v['specialist'].lower() == 'cardiologist']
        if cardio_visits:
            latest = sorted(cardio_visits, key=lambda x: x['date'], reverse=True)[0]
            return {
                "answer": f"Your last cardiologist visit was on {latest['date']} for: {latest['notes']}",
                "data": latest,
                "confidence": 0.8
            }
    
    # Default response
    return {
        "answer": "I couldn't find a specific answer to your question in your records.",
        "data": None,
        "confidence": 0.3
    }

# Uncomment if you want to use OpenAI

def answer_with_gemini(question, patient_data):
    """Generate answers using Gemini, with a confidence score."""
    try:
       
        prompt = (
            "You are a medical assistant. Answer the patient's question using ONLY the following data.\n\n"
            f"PATIENT DATA:\n{json.dumps(patient_data, indent=2)}\n\n"
            f"QUESTION: {question}\n\n"
            "RULES:\n"
            "- Be concise and factual\n"
            "- If information isn't available, say \"Not in records\"\n"
            "- Never invent data"
        )

        # Call Gemini
        response = model.generate_content(prompt)

        # Extract the top candidate’s avgLogprobs (a negative number)
        avg_logprob = None
        if hasattr(response, "candidates") and response.candidates:
            avg_logprob = response.candidates[0].avg_logprobs  # average log‑prob per token

        # Convert to a [0,1] confidence score; exp(logprob) ≈ per‑token probability
        confidence = math.exp(avg_logprob) if avg_logprob is not None else 0.0

        return {
            "answer": response.text,
            "source": "Google Gemini",
            "confidence": round(confidence, 2)
        }
    except Exception as e:
        return {
            "answer": f"Error: {e}",
            "confidence": 0.0
        }
   

@app.route('/api/query', methods=['POST'])
def handle_query():
    try:
        if request.method == "OPTIONS":
            return jsonify({"status": "success"}), 200
            
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
            
        with open('mock_patient_data.json') as f:
            patient_data = json.load(f)
        question = request.json.get('question', '')
        
        if not question:
            return jsonify({"error": "Question is required"}), 400
    
        # Choose one of these approaches:
        # response = answer_question_without_llm(question) # Uncomment to use data based approach
        response = answer_with_gemini(question, patient_data)  
    
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)