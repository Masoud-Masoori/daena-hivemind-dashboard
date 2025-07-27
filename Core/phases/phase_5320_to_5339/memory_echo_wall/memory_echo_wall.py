# memory_echo_wall.py

class MemoryEchoWall:
    def __init__(self):
        self.echo = []

    def push(self, memory_unit):
        self.echo.append(memory_unit)
        if len(self.echo) > 10:
            self.echo.pop(0)

    def reflect(self):
        return self.echo
