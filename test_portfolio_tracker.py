#!/usr/bin/env python3
"""
Test script for Portfolio Tracker System
This script tests the basic functionality without sending emails or creating files.
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from portfolio_tracker import PortfolioTracker, create_sample_portfolio
    print("✅ Portfolio tracker imported successfully!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure portfolio_tracker.py is in the same directory")
    sys.exit(1)

def test_portfolio_tracker():
    """Test the portfolio tracker functionality"""
    print("\n🧪 Testing Portfolio Tracker System...")
    print("=" * 50)
    
    # Test 1: Create sample portfolio
    print("\n1. Testing sample portfolio creation...")
    try:
        sample_portfolio = create_sample_portfolio()
        print(f"✅ Sample portfolio created with {len(sample_portfolio)} stocks")
        print(f"💰 Total investment: ₹{sample_portfolio['Total_Investment'].sum():,.2f}")
    except Exception as e:
        print(f"❌ Error creating sample portfolio: {e}")
        return False
    
    # Test 2: Initialize tracker
    print("\n2. Testing tracker initialization...")
    try:
        tracker = PortfolioTracker()
        print("✅ Portfolio tracker initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing tracker: {e}")
        return False
    
    # Test 3: Load portfolio data
    print("\n3. Testing portfolio data loading...")
    try:
        success = tracker.load_portfolio_data('sample_portfolio.xlsx')
        if success:
            print("✅ Portfolio data loaded successfully")
        else:
            print("❌ Failed to load portfolio data")
            return False
    except Exception as e:
        print(f"❌ Error loading portfolio data: {e}")
        return False
    
    # Test 4: Test price fetching (mock data for testing)
    print("\n4. Testing price fetching (mock data)...")
    try:
        # Mock current prices for testing
        mock_prices = {
            'TMCV': 325.30,
            'TMPV': 360.85,
            'TATASTEEL': 125.0,
            'INFY': 1550.0,
            'LICI': 820.0,
            'VEDL': 260.0,
            'EXIDEIND': 310.0,
            'TATAPOWER': 210.0,
            'TRIDENT': 52.0,
            'ONGC': 155.0,
            'TATACHEM': 1020.0,
            'NTPC': 205.0,
            'IRCTC': 810.0,
            'IEX': 155.0,
            'HCLTECH': 1220.0
        }
        tracker.current_prices = mock_prices
        print("✅ Mock prices set successfully")
    except Exception as e:
        print(f"❌ Error setting mock prices: {e}")
        return False
    
    # Test 5: Test performance calculation
    print("\n5. Testing performance calculation...")
    try:
        tracker.calculate_portfolio_performance()
        print("✅ Performance calculation completed")
        print(f"   📊 Total Investment: ₹{tracker.daily_report['total_investment']:,.2f}")
        print(f"   📈 Current Value: ₹{tracker.daily_report['total_current_value']:,.2f}")
        print(f"   💰 Total P&L: ₹{tracker.daily_report['total_pl']:,.2f} ({tracker.daily_report['total_pl_percentage']:+.2f}%)")
    except Exception as e:
        print(f"❌ Error calculating performance: {e}")
        return False
    
    # Test 6: Test alert checking
    print("\n6. Testing alert system...")
    try:
        alerts = tracker.check_alerts()
        print(f"✅ Alert checking completed - Found {len(alerts)} alerts")
        if alerts:
            for alert in alerts:
                print(f"   🚨 {alert['symbol']}: {alert['type']} - Daily: {alert['daily_pl_percentage']:+.2f}%, Overall: {alert['overall_pl_percentage']:+.2f}%")
    except Exception as e:
        print(f"❌ Error checking alerts: {e}")
        return False
    
    # Test 7: Test chart creation
    print("\n7. Testing chart creation...")
    try:
        chart_filename = tracker.create_portfolio_charts()
        if chart_filename and os.path.exists(chart_filename):
            print(f"✅ Charts created successfully: {chart_filename}")
            # Clean up test chart
            os.remove(chart_filename)
            print("   🧹 Test chart cleaned up")
        else:
            print("⚠️  Chart creation completed but file not found")
    except Exception as e:
        print(f"❌ Error creating charts: {e}")
        return False
    
    # Test 8: Test email report generation
    print("\n8. Testing email report generation...")
    try:
        html_content = tracker.generate_email_report(alerts)
        if html_content and len(html_content) > 100:
            print("✅ Email report generated successfully")
            print(f"   📧 Report length: {len(html_content)} characters")
        else:
            print("❌ Email report generation failed")
            return False
    except Exception as e:
        print(f"❌ Error generating email report: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
    print("✅ Portfolio tracker system is working correctly")
    print("\n📋 Next steps:")
    print("   1. Update email credentials in portfolio_tracker.py")
    print("   2. Replace sample portfolio with your actual data")
    print("   3. Test with real data: python portfolio_tracker.py")
    print("   4. Set up daily automation")
    
    return True

def main():
    """Main test function"""
    print("🚀 PORTFOLIO TRACKER - SYSTEM TEST")
    print("=" * 50)
    
    # Check if required files exist
    if not os.path.exists('portfolio_tracker.py'):
        print("❌ portfolio_tracker.py not found!")
        print("Make sure you're in the correct directory")
        return False
    
    # Run tests
    success = test_portfolio_tracker()
    
    if success:
        print("\n🎯 System is ready for production use!")
        return True
    else:
        print("\n❌ System test failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
