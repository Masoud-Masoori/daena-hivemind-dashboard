# meta_prompt_enforcer.py
class MetaPromptEnforcer:
    def enforce(self, prompt, mission_statement):
        if mission_statement.lower() not in prompt.lower():
            return f"{mission_statement}\n\n{prompt}"
        return prompt
