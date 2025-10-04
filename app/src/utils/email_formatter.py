from datetime import datetime
import pandas as pd

def create_newsletter_content(tickers: list[str]) -> str:
    """Create the newsletter content with news and metrics."""
    import sys
    import io
    from src.data.news_data import get_all_news
    from src.data.stock_data import extract_metrics

    current_date = datetime.now().strftime("%B %d, %Y")

    # Get news placeholder data
    news_data = get_all_news(tickers)

    # Suppress print output from extract_metrics
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        metrics_df = extract_metrics(tickers)
    finally:
        sys.stdout = old_stdout

    content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h2 {{ color: #2c3e50; }}
            h3 {{ color: #34495e; margin-top: 30px; }}
            .ticker-section {{ margin-bottom: 30px; border-left: 4px solid #3498db; padding-left: 15px; }}
            .ticker-name {{ font-size: 20px; font-weight: bold; color: #2980b9; }}
            .news-list {{ margin: 10px 0; }}
            .news-item {{ margin: 5px 0; color: #555; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th {{ background-color: #3498db; color: white; padding: 8px 6px; text-align: left; }}
            td {{ padding: 6px 4px; border-bottom: 1px solid #ddd; }}
            tr:hover {{ background-color: #f5f5f5; }}
            .positive {{ color: green; }}
            .negative {{ color: red; }}
        </style>
    </head>
    <body>
        <h2>Portfolio Newsletter</h2>
        <p><strong>Daily portfolio update for: {", ".join(tickers)}</strong></p>
        <p><em>Generated on {current_date}</em></p>

        <h3>Stock News & Updates</h3>
    """

    # Add news section for each ticker
    for ticker in tickers:
        news_items = news_data.get(ticker, [])
        content += f"""
        <div class="ticker-section">
            <div class="ticker-name">{ticker}</div>
            <ul class="news-list">
        """
        for news_item in news_items:
            content += (
                f'                <li class="news-item">{news_item}</li>\n'
            )
        content += """
            </ul>
        </div>
        """

    # Add metrics section
    content += """
        <h3>Key Metrics</h3>
        <table>
            <thead>
                <tr>
                    <th>Ticker</th>
                    <th>Volatility (10d %)</th>
                    <th>SMA 50d Ratio</th>
                    <th>Momentum (10d %)</th>
                    <th>Volume Ratio (10d)</th>
                </tr>
            </thead>
            <tbody>
    """

    # Add metrics rows
    for _, row in metrics_df.iterrows():
        ticker = row["Ticker"]
        volatility = (
            row["Volatility (10d %)"]
            if pd.notna(row["Volatility (10d %)"])
            else "N/A"
        )
        sma_ratio = (
            row["SMA 50d Ratio"]
            if pd.notna(row["SMA 50d Ratio"])
            else None
        )
        momentum = (
            row["Momentum (10d %)"]
            if pd.notna(row["Momentum (10d %)"])
            else None
        )
        volume_ratio = (
            row["Volume Ratio (10d)"]
            if pd.notna(row["Volume Ratio (10d)"])
            else "N/A"
        )

        # Format SMA ratio with color
        if sma_ratio is not None:
            sma_class = "positive" if sma_ratio >= 1.0 else "negative"
            sma_display = f'<span class="{sma_class}">{sma_ratio:.2f}x</span>'
        else:
            sma_display = "N/A"

        # Format momentum with color
        if momentum is not None:
            momentum_class = "positive" if momentum >= 0 else "negative"
            momentum_display = (
                f'<span class="{momentum_class}">{momentum:+.2f}%</span>'
            )
        else:
            momentum_display = "N/A"

        content += f"""
                <tr>
                    <td><strong>{ticker}</strong></td>
                    <td>{volatility if volatility == 'N/A' else f'{volatility:.2f}%'}</td>
                    <td>{sma_display}</td>
                    <td>{momentum_display}</td>
                    <td>{volume_ratio if volume_ratio == 'N/A' else f'{volume_ratio:.2f}x'}</td>
                </tr>
        """

    content += """
            </tbody>
        </table>

        <div style="margin-top: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 5px;">
            <h4 style="margin-top: 0; color: #34495e;">Metrics Definitions</h4>
            <ul style="font-size: 14px; color: #555; line-height: 1.6;">
                <li><strong>Volatility (10d %):</strong> Price range over 10 days, calculated as ((high - low) / low) × 100</li>
                <li><strong>SMA 50d Ratio:</strong> Current price divided by 50-day Simple Moving Average (>1.0 = above SMA, <1.0 = below SMA)</li>
                <li><strong>Momentum (10d %):</strong> 10-day price change percentage, showing recent trend direction</li>
                <li><strong>Volume Ratio (10d):</strong> Current volume relative to 10-day average volume</li>
            </ul>
        </div>

        <p style="margin-top: 30px;"><em>This is an automated newsletter generated by Clément Van Goethem</em></p>
    </body>
    </html>
    """

    return content.strip()
