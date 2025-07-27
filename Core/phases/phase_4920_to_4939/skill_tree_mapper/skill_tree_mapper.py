# skill_tree_mapper.py
class SkillTree:
    def __init__(self, domain):
        self.domain = domain
        self.skills = {}

    def add_skill(self, level, skill):
        if level not in self.skills:
            self.skills[level] = []
        self.skills[level].append(skill)

    def get_map(self):
        return self.skills
