# emotional_reply_weighter.py

def apply_emotional_weight(response, tone_intensity):
    if 'confidence' in response:
        response['confidence'] *= (1 + tone_intensity * 0.1)
    print(f"[Emotion]  Adjusted confidence to {response['confidence']:.2f} with tone {tone_intensity}")
    return response
