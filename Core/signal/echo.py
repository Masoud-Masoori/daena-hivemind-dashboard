class ContinuitySignalEcho:
    def __init__(self, interval=5):
        self.interval = interval
        self.echo_count = 0

    def echo(self):
        self.echo_count += 1
        print(f" Echo {self.echo_count}: Continuing mission path.")
