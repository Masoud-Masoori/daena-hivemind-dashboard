def validate_source(trace):
    return all("source" in step for step in trace)

if __name__ == "__main__":
    print("[Traceability] :", validate_source([{"source": "web"}, {"source": "pdf"}]))
