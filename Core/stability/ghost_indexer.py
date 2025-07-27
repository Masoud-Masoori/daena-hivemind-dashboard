def index_archives(archive_list):
    ghost_tags = [a for a in archive_list if "ghost" in a]
    return {"ghost_indexed": ghost_tags, "total": len(ghost_tags)}

if __name__ == "__main__":
    archives = ["log_alpha", "ghost_core", "ghost_vision", "mission_final"]
    print("[GhostIndexer] ", index_archives(archives))
