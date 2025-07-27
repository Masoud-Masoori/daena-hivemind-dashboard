# blackbox_detour_controller.py
class BlackboxDetourController:
    def __init__(self):
        self.unexpected_routes = []

    def log_unexpected_path(self, function_name):
        self.unexpected_routes.append(function_name)
        return f" Detour logged: {function_name}"

    def get_logs(self):
        return self.unexpected_routes
