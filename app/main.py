import os


def main():
    """
    A simple application that logs a success message
    """
    print("--- Portfolio Newsletter Job ---")
    print("Job started successfully!")

    # READ IN TICKERS
    tickers = os.getenv("TICKERS")

    newsletter = ""

    newsletter += "Start detecting stock price changes\n"
    detect_stock_price_changes(tickers)
    newsletter += "Start detecting news\n"
    detect_news(tickers)

    print(newsletter)

    print("Job finished.")

if __name__ == "__main__":
    main()

