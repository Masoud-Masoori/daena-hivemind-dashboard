class FreelanceMarketBridge:
    def __init__(self):
        self.sources = ["Fiverr", "Upwork", "Freelancer"]

    def fetch_projects(self):
        print(" Scanning freelance sites for tasks...")
        return [{"title": "React App", "budget": "$500"}, {"title": "AI chatbot", "budget": "$300"}]
