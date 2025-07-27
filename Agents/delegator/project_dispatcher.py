import uuid, json

class Dispatcher:
    def __init__(self):
        self.projects = []

    def create_project(self, title, subtasks):
        proj_id = str(uuid.uuid4())
        project = {"id": proj_id, "title": title, "subtasks": subtasks}
        self.projects.append(project)
        for task in subtasks:
            task["assigned_to"] = "AutoSelector"  # Fill later
        return project

# Example
dispatcher = Dispatcher()
dispatcher.create_project("Revenue Forecasting", [{"type": "collect_data"}, {"type": "predict"}])
