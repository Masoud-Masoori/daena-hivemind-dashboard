import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from core.wake_loop import wake_loop

if __name__ == "__main__":
    wake_loop()
