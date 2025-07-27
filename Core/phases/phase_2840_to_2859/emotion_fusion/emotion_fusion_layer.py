# emotion_fusion_layer.py

def fuse_emotions(input_data):
    scores = {
        'joy': input_data.count(''),
        'anger': input_data.count(''),
        'sadness': input_data.count(''),
        'neutral': input_data.count('.') + input_data.count('...')
    }
    dominant = max(scores, key=scores.get)
    print(f"[EmotionFusion]  Dominant emotion detected: {dominant}")
    return dominant
