from flask import Flask, request, jsonify
import os
import logging
import json
from s2t import speech_to_text
from sentiment_analysis import analyze_sentiment
from session_recommendation import session_recommendation

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load voice data
VOICE_DATA = []
try:
    with open('voice_data.json') as f:
        VOICE_DATA = json.load(f)
except Exception as e:
    logger.warning(f"Couldn't load voice data: {e}")

def get_historical_data(participant_id: str) -> list:
    return [entry for entry in VOICE_DATA if entry['participant_id'] == participant_id]

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"}) # Match Postman output

@app.route('/analyze', methods=['POST'])
def analyze_session():
    try:
        if 'participant_id' not in request.form:
            return jsonify({"error": "Missing participant_id"}), 400
            
        participant_id = request.form['participant_id']
        therapy_progress = float(request.form.get('therapy_progress', 0.5))
        trauma_history = request.form.get('trauma_history', 'false').lower() == 'true'
        text_feedback = request.form.get('text_feedback', '')
        audio_file = request.files.get('audio_file')

        if not 0.0 <= therapy_progress <= 1.0:
            return jsonify({"error": "Invalid therapy_progress"}), 400

        voice_text = ""
        if audio_file and audio_file.filename:
            try:
                os.makedirs('recordings', exist_ok=True)
                filename = f"recordings/{audio_file.filename}"
                audio_file.save(filename)
                voice_text = speech_to_text(filename) or "" # Handle None case
                os.remove(filename)
            except Exception as e:
                logger.error(f"Audio processing error: {e}")

        combined_text = f"{text_feedback} {voice_text}".strip()
        sentiment = analyze_sentiment(combined_text)
        
        return jsonify({
            "sentiment_score": sentiment.upper(), # Match Postman output
            "recommendations": {
                "activity": session_recommendation(sentiment),
                "duration": "30min", # Static for simplicity; adjust as needed
                "intensity": "medium", # Static; could be dynamic
                "progress_metrics": therapy_progress,
                "recommendation_score": round(therapy_progress * 2, 2), # Example metric
                "trauma_sensitive": trauma_history
            },
            "status": "success",
            "therapist_insights": {
                "participant_id": participant_id,
                "sentiment_trends": {
                    "current": sentiment,
                    "previous": [entry['sentiment'] for entry in get_historical_data(participant_id)]
                },
                "session_count": len(get_historical_data(participant_id)) + 1,
                "therapy_progress": therapy_progress,
                "trauma_correlation": trauma_history
            }
        })
        
    except Exception as e:
        logger.error(f"Server error: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
