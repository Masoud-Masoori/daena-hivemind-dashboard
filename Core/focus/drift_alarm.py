class FocusDriftAlarm:
    def __init__(self, max_idle_steps=3):
        self.idle_counter = 0
        self.max_idle = max_idle_steps

    def tick(self, current_action):
        if current_action == "unfocused":
            self.idle_counter += 1
        else:
            self.idle_counter = 0

        if self.idle_counter >= self.max_idle:
            print(" Focus drift detected! Refocus needed.")
            return True
        return False
