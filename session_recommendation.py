import random

def session_recommendation(sentiment):
    #sentiment=sentiment.lower()
    """
    Generate personalized therapy session recommendations based on sentiment (positive, neutral, or negative).
    
    Arguments:
    sentiment : str : 'positive', 'neutral', 'negative'
    
    Returns:
    str : Suggested activity or therapy session adjustment.
    """
    
    # Define activity categories
    calming_activities = [
        "Grooming the horse",
        "Slow-paced riding in a calm area",
        "Breathing exercises with the horse",
        "Gentle stretching and massage with the horse",
        "Sitting with the horse in a quiet place"
    ]
    
    engaging_activities = [
        "Trotting",
        "Obstacle course with light exercises",
        "Interactive training: teaching the horse tricks",
        "Group therapy activities and team-building with the horse",
        "Agility and jumping drills"
    ]
    
    neutral_activities = [
        "Continue with the current therapy plan",
        "Engage in light exercises without specific changes"
    ]
    
    # Sentiment-based activity recommendation
    if sentiment == "negative":
        activity = random.choice(calming_activities)
        return f"Sentiment is negative. Recommended calming activity: {activity}"

    elif sentiment == "positive":
        activity = random.choice(engaging_activities)
        return f"Sentiment is positive. Recommended engaging activity: {activity}"

    elif sentiment == "neutral":
        activity = random.choice(neutral_activities)
        return f"Sentiment is neutral. Continue with the session as planned: {activity}"

    else:
        return "Error: Sentiment not recognized. Please provide a valid sentiment (e.g., 'positive', 'negative')."

# Example Tests
#print(session_recommendation('negative'))
#print(session_recommendation('positive'))
#print(session_recommendation('neutral'))