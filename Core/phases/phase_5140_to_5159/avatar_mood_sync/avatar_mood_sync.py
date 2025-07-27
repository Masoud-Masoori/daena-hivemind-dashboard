# avatar_mood_sync.py
class AvatarMoodSync:
    def get_mood_color(self, emotion):
        return {
            "happy": "#FFFF66",
            "sad": "#66B2FF",
            "angry": "#FF6666",
            "neutral": "#CCCCCC"
        }.get(emotion, "#CCCCCC")

    def update_avatar(self, emotion):
        color = self.get_mood_color(emotion)
        print(f"Avatar mood color updated to: {color}")
