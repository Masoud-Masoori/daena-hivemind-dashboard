class FreelanceAgent:
    def __init__(self, name):
        self.name = name

    def scan_skills(self):
        return ["Python", "Web", "AI", "ML"]

    def propose_projects(self):
        print(f"[AGENT:{self.name}] Proposing freelance opportunities...")
        for skill in self.scan_skills():
            print(f"-> {skill}-based automation service")

if __name__ == '__main__':
    agent = FreelanceAgent("HelixAgent")
    agent.propose_projects()
