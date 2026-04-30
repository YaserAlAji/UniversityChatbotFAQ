import os
import sys

# Ensure the backend module can be found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.train_bot import train_bot

if __name__ == '__main__':
    train_bot()
