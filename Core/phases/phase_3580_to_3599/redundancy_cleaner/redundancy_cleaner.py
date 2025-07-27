# redundancy_cleaner.py
def clean_redundant(entries):
    return list(dict.fromkeys(entries))
