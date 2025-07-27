def finalize_narrative(narrative_segments):
    return "[Narrative]  Finalized: " + " ".join(narrative_segments).strip().capitalize() + "."

if __name__ == "__main__":
    print(finalize_narrative(["daena started", "the deployment successfully", "with no critical warnings"]))
