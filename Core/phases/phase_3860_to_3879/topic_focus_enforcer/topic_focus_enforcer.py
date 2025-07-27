# topic_focus_enforcer.py
class TopicFocusEnforcer:
    def __init__(self):
        self.target_topic = None

    def set_topic(self, topic):
        self.target_topic = topic

    def reinforce(self, new_topic):
        if self.target_topic and new_topic != self.target_topic:
            return f"Lets refocus on our main topic: {self.target_topic}"
        return None
