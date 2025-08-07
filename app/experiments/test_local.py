import os
import sys

# Add the parent directory (app) to the Python path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import core

if __name__ == "__main__":
    result = core.generate_newsletter(["AAPL", "GOOGL", "MSFT"], ["jason.m.kang@gmail.com"])
    print(result)
