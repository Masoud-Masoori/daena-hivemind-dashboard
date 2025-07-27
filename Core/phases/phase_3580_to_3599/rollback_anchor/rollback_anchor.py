# rollback_anchor.py
def create_anchor(snapshot):
    return {"rollback_id": hash(str(snapshot)), "snapshot": snapshot}
