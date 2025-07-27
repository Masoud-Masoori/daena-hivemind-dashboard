def generate_temporal_nodes(sequence, rate=1):
    return [f"[TemporalNode]  {i * rate}" for i in range(len(sequence))]

if __name__ == "__main__":
    print(generate_temporal_nodes(["a", "ß", "?"], rate=5))
