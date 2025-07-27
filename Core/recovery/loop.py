class AttentionRecoveryLoop:
    def recover(self, logs):
        print(" Rebuilding attention from logs...")
        for entry in logs[-5:]:
            print(f" {entry}")
