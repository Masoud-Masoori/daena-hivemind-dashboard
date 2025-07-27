import random
def break_tie(tied_items):
    return random.choice(tied_items) if tied_items else None
