def resolve_memory_trace(trace):
    if not trace:
        return "[MemoryResolver]  Empty trace."
    return f"[MemoryResolver] Trace Resolved: {trace[:30]}..."

if __name__ == "__main__":
    print(resolve_memory_trace("...interrupted reasoning segment..."))
