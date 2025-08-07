#!/usr/bin/env python3
"""
Simple test script for the price change detection functionality
"""
import sys 
import os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.experiments.stock_prices.price_change_detection import analyze_stock_prices

def test_price_detection():
    """Test the price change detection with some popular stocks"""
    
    # Test with some popular tickers
    test_tickers = "AAPL,GOOGL,MSFT,TSLA"
    
    print("Testing price change detection...")
    print(f"Tickers: {test_tickers}")
    
    try:
        results = analyze_stock_prices(test_tickers, days=10)
        
        print("\nResults:")
        for ticker, data in results.items():
            if 'error' in data:
                print(f"{ticker}: ERROR - {data['error']}")
            else:
                print(f"{ticker}:")
                print(f"  Current Price: ${data['current_price']:.2f}")
                print(f"  % Change (10 days): {data['percentage_change']:.2f}%")
                print(f"  Volatility: {data['volatility']:.2f}")
                print(f"  Days Analyzed: {data['days_analyzed']}")
        
        print(f"\nSuccessfully analyzed {len(results)} tickers")
        
    except Exception as e:
        print(f"Error during testing: {e}")


if __name__ == "__main__":
    test_price_detection() 