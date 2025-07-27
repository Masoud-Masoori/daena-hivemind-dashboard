# recursive_planner_agent.py

class RecursivePlannerAgent:
    def plan(self, goal, depth=3):
        if depth == 0:
            return [f"Execute: {goal}"]
        return [f"Step {depth} to reach {goal}"] + self.plan(goal, depth - 1)
