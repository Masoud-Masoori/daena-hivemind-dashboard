# memory_split_tracer.py
import uuid
memory_branches = {}

def trace_memory_branch(source, fork_info):
    branch_id = str(uuid.uuid4())
    memory_branches[branch_id] = {
        "source": source,
        "fork": fork_info
    }
    return branch_id

def get_branch(branch_id):
    return memory_branches.get(branch_id, {})
