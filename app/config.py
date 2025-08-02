import os

import dotenv

dotenv.load_dotenv()

TICKERS = os.getenv("TICKERS")
