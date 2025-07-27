def validate_instructions(instr_list):
    all_consistent = all(":" in i for i in instr_list)
    return f"[InstructionCheck]  All consistent: {all_consistent}"

if __name__ == "__main__":
    print(validate_instructions(["Load: Memory", "Execute: Action", "Save: State"]))
