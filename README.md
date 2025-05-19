Mini MedQuery System
===================

A lightweight medical query system that allows users to ask natural language questions about their health records, with responses generated from either direct data lookup or Google Gemini AI.

Features
--------
- Natural language query interface
- Two response modes:
  * Direct data lookup (high confidence)
  * AI-generated answers (Gemini-powered)
- Confidence scoring for all responses
- CORS-enabled Flask backend
- React frontend

Setup Instructions
------------------

Prerequisites:
- Python 3.9+
- Node.js 16+
- Google Gemini API key (optional for AI mode)

Backend Setup:
1. Navigate to the backend directory:
   cd backend

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows

3. Install dependencies:
   pip install -r requirements.txt

4. Create .env file for Gemini (optional):
   echo "GEMINI_API_KEY=your_api_key_here" > .env

5. Run the backend:
   python app.py
   (Server starts at http://localhost:5001)

Frontend Setup:
1. In a new terminal, navigate to frontend:
   cd frontend

2. Install dependencies:
   npm install

3. Run the development server:
   npm start
   (App launches at http://localhost:3000)

Configuration Options
--------------------

Switching Response Modes:
Modify backend/app.py:
# Uncomment your preferred method:
response = answer_question_without_llm(question)  # Direct lookup
# response = answer_with_gemini(question, patient_data)  # Gemini AI

Customizing Confidence Thresholds:
Edit these values in backend/app.py:
# In answer_question_without_llm():
base_confidence = 0.9  # For direct matches
recency_confidence = max(0.9 - (days_old / 365 * 0.5), 0.5)

# In answer_with_gemini():
"confidence": float(result.get("confidence", 0.7))  # Default AI confidence

Query Examples
-------------
Try these sample questions:
- "What medications am I taking?"
- "When was my last cholesterol test?"
- "Explain my hypertension diagnosis"
- "What did my cardiologist recommend?"
- "What health events occurred in January 2024?"
- "Show me all records from the last 6 months"
- "What medications am I taking for diabetes?"
- "How long have I had high cholesterol?"


Response Interpretation
----------------------
All responses include:
- answer: The generated response
- confidence: Score from 0 (low) to 1 (high)




Troubleshooting
--------------

Common Issues:
1. CORS Errors: Ensure backend has CORS(app) configured
2. Gemini API Failures:
   - Verify API key in .env
   - Check quota at Google AI Studio
3. Port Conflicts:
   lsof -i :5001  # Check backend port
   lsof -i :3000  # Check frontend port



License
-------
MIT License
