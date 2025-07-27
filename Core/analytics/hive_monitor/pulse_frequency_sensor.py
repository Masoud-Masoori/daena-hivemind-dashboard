def frequency_sensor(signal_list):
    return {"average": sum(signal_list)/len(signal_list), "high": max(signal_list), "low": min(signal_list)}

if __name__ == "__main__":
    print("[PulseFreq] ", frequency_sensor([1.2, 2.4, 1.8]))
