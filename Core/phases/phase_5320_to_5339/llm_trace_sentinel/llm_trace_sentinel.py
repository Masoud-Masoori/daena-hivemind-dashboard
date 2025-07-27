# llm_trace_sentinel.py

class LLMTraceSentinel:
    def __init__(self):
        self.trace_log = []

    def record(self, prompt, response):
        self.trace_log.append({"prompt": prompt, "response": response})

    def last_trace(self):
        return self.trace_log[-5:] if self.trace_log else []
