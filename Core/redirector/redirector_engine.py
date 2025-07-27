class Redirector:
    def __init__(self, goal_path):
        self.goal_path = goal_path

    def re_align(self, current_state):
        print(f" Redirecting back to goal path: {self.goal_path}")
        return self.goal_path
