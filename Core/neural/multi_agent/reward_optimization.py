def reward_score(output_quality, efficiency):
    return round((output_quality * 0.7 + efficiency * 0.3), 2)

if __name__ == "__main__":
    print("[Reward] ", reward_score(8.7, 6.2))
