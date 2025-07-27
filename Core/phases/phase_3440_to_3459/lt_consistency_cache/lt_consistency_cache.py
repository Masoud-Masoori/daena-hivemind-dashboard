# lt_consistency_cache.py

import json
from pathlib import Path

cache_path = Path('D:/Ideas/Daena/core/cache/lt_cache.json')
cache_data = {}

def save_result(key, result):
    cache_data[key] = result
    with cache_path.open('w', encoding='utf-8') as f:
        json.dump(cache_data, f, indent=2)

def retrieve_result(key):
    return cache_data.get(key, None)
