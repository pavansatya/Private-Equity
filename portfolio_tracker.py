#!/usr/bin/env python3
"""
Automated Portfolio Tracker System
This system will run daily to track your portfolio performance and send email reports.

Features:
- Daily portfolio performance tracking
- Real-time price updates via Yahoo Finance
- P&L alerts for stocks outside ±5% threshold
- Automated daily email reports with charts
- Excel file updates and performance history
- Portfolio visualization charts
"""

import pandas as pd
import numpy as np
import yfinance as yf
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
import os
import sys

warnings.filterwarnings('ignore')

# Your portfolio configuration
PORTFOLIO_LIST = ['TATAMOTORS', 'TATASTEEL', 'INFY', 'LICI', 'VEDL', 'EXIDEIND', 
                  'TATAPOWER', 'TRIDENT', 'ONGC', 'TATACHEM', 'NTPC', 'IRCTC', 
                  'IEX', 'HCLTECH']

# Email configuration (UPDATE THESE WITH YOUR CREDENTIALS)
EMAIL_SENDER = "email@gmail.com"  # Replace with your Gmail
EMAIL_PASSWORD = "PASSWORD"    # Replace with your Gmail App Password
EMAIL_RECEIVER = "email@gmail.com" # Replace with your email
REPORT_TIME = "TIME"  # 5:00 AM CST
ALERT_THRESHOLD = "Percentage"  # Alert for P&L outside ±5%

class PortfolioTracker:
    def __init__(self):
        self.portfolio_data = None
        self.current_prices = {}
        self.daily_report = {}
        
    def load_portfolio_data(self, excel_file_path):
        """Load portfolio data from Excel file"""
        try:
            self.portfolio_data = pd.read_excel(excel_file_path)
            print(f"✅ Portfolio data loaded successfully from {excel_file_path}")
            print(f"📊 Found {len(self.portfolio_data)} stocks in portfolio")
            return True
        except Exception as e:
            print(f"❌ Error loading portfolio data: {e}")
            return False
    
    def get_current_prices(self):
        """Fetch current market prices for portfolio stocks"""
        print("🔄 Fetching current market prices...")
        
        for symbol in PORTFOLIO_LIST:
            try:
                # Add .NS suffix for NSE stocks
                ticker = yf.Ticker(f"{symbol}.NS")
                current_price = ticker.info.get('regularMarketPrice', 0)
                
                if current_price:
                    self.current_prices[symbol] = current_price
                    print(f"✅ {symbol}: ₹{current_price:.2f}")
                else:
                    print(f"⚠️  {symbol}: Price not available")
                    
            except Exception as e:
                print(f"❌ Error fetching price for {symbol}: {e}")
        
        print(f"📈 Successfully fetched prices for {len(self.current_prices)} stocks")
    
    def calculate_portfolio_performance(self):
        """Calculate current portfolio performance metrics"""
        if self.portfolio_data is None:
            print("❌ Portfolio data not loaded")
            return
        
        print("🧮 Calculating portfolio performance...")
        
        # Merge current prices with portfolio data
        self.portfolio_data['Current_Price'] = self.portfolio_data['Stock_Symbol'].map(self.current_prices)
        
        # Calculate performance metrics
        self.portfolio_data['Current_Value'] = self.portfolio_data['Current_Price'] * self.portfolio_data['Quantity']
        self.portfolio_data['Total_Investment'] = self.portfolio_data['Purchase_Price'] * self.portfolio_data['Quantity']
        self.portfolio_data['Unrealized_PL'] = self.portfolio_data['Current_Value'] - self.portfolio_data['Total_Investment']
        self.portfolio_data['PL_Percentage'] = (self.portfolio_data['Unrealized_PL'] / self.portfolio_data['Total_Investment']) * 100
        
        # Calculate portfolio totals
        total_investment = self.portfolio_data['Total_Investment'].sum()
        total_current_value = self.portfolio_data['Current_Value'].sum()
        total_pl = total_current_value - total_investment
        total_pl_percentage = (total_pl / total_investment) * 100
        
        self.daily_report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'total_investment': total_investment,
            'total_current_value': total_current_value,
            'total_pl': total_pl,
            'total_pl_percentage': total_pl_percentage,
            'portfolio_data': self.portfolio_data.copy()
        }
        
        print(f"📊 Portfolio Summary:")
        print(f"   Total Investment: ₹{total_investment:,.2f}")
        print(f"   Current Value: ₹{total_current_value:,.2f}")
        print(f"   Total P&L: ₹{total_pl:,.2f} ({total_pl_percentage:+.2f}%)")
    
    def check_alerts(self):
        """Check for stocks outside alert threshold"""
        alerts = []
        
        for _, row in self.portfolio_data.iterrows():
            pl_percentage = row['PL_Percentage']
            if abs(pl_percentage) > ALERT_THRESHOLD:
                alert_type = "🔴 LOSS ALERT" if pl_percentage < -ALERT_THRESHOLD else "🟢 PROFIT ALERT"
                alerts.append({
                    'symbol': row['Stock_Symbol'],
                    'type': alert_type,
                    'pl_percentage': pl_percentage,
                    'current_price': row['Current_Price']
                })
        
        return alerts
    
    def create_portfolio_charts(self):
        """Create portfolio visualization charts"""
        try:
            # Set style
            plt.style.use('default')
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Pie chart of holdings by value
            portfolio_by_value = self.portfolio_data.groupby('Stock_Symbol')['Current_Value'].sum()
            ax1.pie(portfolio_by_value.values, labels=portfolio_by_value.index, autopct='%1.1f%%')
            ax1.set_title('Portfolio Allocation by Current Value', fontsize=14, fontweight='bold')
            
            # Bar chart of P&L by stock
            colors = ['green' if x >= 0 else 'red' for x in self.portfolio_data['PL_Percentage']]
            ax2.bar(self.portfolio_data['Stock_Symbol'], self.portfolio_data['PL_Percentage'], color=colors)
            ax2.set_title('Individual Stock P&L (%)', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Stock Symbol')
            ax2.set_ylabel('P&L Percentage (%)')
            ax2.tick_params(axis='x', rotation=45)
            ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            ax2.axhline(y=ALERT_THRESHOLD, color='orange', linestyle='--', alpha=0.7, label=f'+{ALERT_THRESHOLD}% Alert')
            ax2.axhline(y=-ALERT_THRESHOLD, color='orange', linestyle='--', alpha=0.7, label=f'-{ALERT_THRESHOLD}% Alert')
            ax2.legend()
            
            plt.tight_layout()
            
            # Save chart
            chart_filename = f"portfolio_chart_{datetime.now().strftime('%Y%m%d')}.png"
            plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"📊 Charts saved as {chart_filename}")
            return chart_filename
            
        except Exception as e:
            print(f"❌ Error creating charts: {e}")
            return None
    
    def generate_email_report(self, alerts, chart_filename=None):
        """Generate comprehensive email report"""
        report_date = datetime.now().strftime('%B %d, %Y')
        
        # Portfolio summary
        summary_html = f"""
        <h2>📊 Daily Portfolio Report - {report_date}</h2>
        <hr>
        <h3>Portfolio Summary</h3>
        <table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
            <tr style="background-color: #f8f9fa;">
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Total Investment</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">₹{self.daily_report['total_investment']:,.2f}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Current Value</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">₹{self.daily_report['total_current_value']:,.2f}</td>
            </tr>
            <tr style="background-color: {'#d4edda' if self.daily_report['total_pl'] >= 0 else '#f8d7da'};">
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>Total P&L</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd; color: {'green' if self.daily_report['total_pl'] >= 0 else 'red'};">
                    ₹{self.daily_report['total_pl']:,.2f} ({self.daily_report['total_pl_percentage']:+.2f}%)
                </td>
            </tr>
        </table>
        """
        
        # Individual stock performance
        stocks_html = """
        <h3>Individual Stock Performance</h3>
        <table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
            <tr style="background-color: #007bff; color: white;">
                <th style="padding: 10px; border: 1px solid #ddd;">Stock</th>
                <th style="padding: 10px; border: 1px solid #ddd;">Current Price</th>
                <th style="padding: 10px; border: 1px solid #ddd;">P&L</th>
                <th style="padding: 10px; border: 1px solid #ddd;">P&L %</th>
            </tr>
        """
        
        for _, row in self.portfolio_data.iterrows():
            pl_color = 'green' if row['PL_Percentage'] >= 0 else 'red'
            stocks_html += f"""
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;"><strong>{row['Stock_Symbol']}</strong></td>
                <td style="padding: 10px; border: 1px solid #ddd;">₹{row['Current_Price']:.2f}</td>
                <td style="padding: 10px; border: 1px solid #ddd; color: {pl_color};">₹{row['Unrealized_PL']:,.2f}</td>
                <td style="padding: 10px; border: 1px solid #ddd; color: {pl_color};">{row['PL_Percentage']:+.2f}%</td>
            </tr>
            """
        
        stocks_html += "</table>"
        
        # Alerts section
        alerts_html = ""
        if alerts:
            alerts_html = f"""
            <h3>🚨 Alerts ({len(alerts)} stocks outside ±{ALERT_THRESHOLD}% threshold)</h3>
            <table style="border-collapse: collapse; width: 100%; margin: 20px 0;">
                <tr style="background-color: #fff3cd;">
                    <th style="padding: 10px; border: 1px solid #ddd;">Stock</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Alert Type</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">P&L %</th>
                </tr>
            """
            
            for alert in alerts:
                alerts_html += f"""
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>{alert['symbol']}</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{alert['type']}</td>
                    <td style="padding: 10px; border: 1px solid #ddd; color: {'green' if alert['pl_percentage'] > 0 else 'red'};">
                        {alert['pl_percentage']:+.2f}%
                    </td>
                </tr>
                """
            
            alerts_html += "</table>"
        
        # Complete HTML
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h2, h3 {{ color: #333; }}
                .positive {{ color: green; }}
                .negative {{ color: red; }}
            </style>
        </head>
        <body>
            {summary_html}
            {stocks_html}
            {alerts_html}
            <hr>
            <p style="color: #666; font-size: 12px;">
                This report was automatically generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} IST<br>
                Portfolio Tracker System - Powered by Python
            </p>
        </body>
        </html>
        """
        
        return html_content
    
    def send_email_report(self, html_content, chart_filename=None):
        """Send email report with optional chart attachment"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"📊 Daily Portfolio Report - {datetime.now().strftime('%Y-%m-%d')}"
            msg['From'] = EMAIL_SENDER
            msg['To'] = EMAIL_RECEIVER
            
            # HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Attach chart if available
            if chart_filename and os.path.exists(chart_filename):
                with open(chart_filename, 'rb') as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-ID', '<portfolio_chart>')
                    img.add_header('Content-Disposition', 'inline', filename=chart_filename)
                    msg.attach(img)
            
            # Send email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)
            
            print(f"✅ Email report sent successfully to {EMAIL_RECEIVER}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def update_portfolio_excel(self, output_filename):
        """Update and save portfolio data to Excel"""
        try:
            # Add timestamp
            self.portfolio_data['Last_Updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Save to Excel
            with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
                # Main portfolio data
                self.portfolio_data.to_excel(writer, sheet_name='Portfolio', index=False)
                
                # Daily summary
                summary_data = pd.DataFrame([{
                    'Date': self.daily_report['date'],
                    'Total_Investment': self.daily_report['total_investment'],
                    'Current_Value': self.daily_report['total_current_value'],
                    'Total_PL': self.daily_report['total_pl'],
                    'Total_PL_Percentage': self.daily_report['total_pl_percentage']
                }])
                summary_data.to_excel(writer, sheet_name='Daily_Summary', index=False)
                
                # Performance history (append to existing)
                try:
                    existing_history = pd.read_excel(output_filename, sheet_name='Performance_History')
                    new_row = pd.DataFrame([{
                        'Date': self.daily_report['date'],
                        'Total_Investment': self.daily_report['total_investment'],
                        'Current_Value': self.daily_report['total_current_value'],
                        'Total_PL': self.daily_report['total_pl'],
                        'Total_PL_Percentage': self.daily_report['total_pl_percentage']
                    }])
                    updated_history = pd.concat([existing_history, new_row], ignore_index=True)
                except:
                    updated_history = summary_data
                
                updated_history.to_excel(writer, sheet_name='Performance_History', index=False)
            
            print(f"✅ Portfolio Excel updated: {output_filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating Excel: {e}")
            return False
    
    def run_daily_tracker(self, portfolio_excel_path, output_excel_path):
        """Main function to run daily portfolio tracking"""
        print("🚀 Starting Daily Portfolio Tracker...")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        # Step 1: Load portfolio data
        if not self.load_portfolio_data(portfolio_excel_path):
            return False
        
        # Step 2: Get current prices
        self.get_current_prices()
        
        # Step 3: Calculate performance
        self.calculate_portfolio_performance()
        
        # Step 4: Check alerts
        alerts = self.check_alerts()
        if alerts:
            print(f"🚨 Found {len(alerts)} alerts:")
            for alert in alerts:
                print(f"   {alert['symbol']}: {alert['type']} - {alert['pl_percentage']:+.2f}%")
        
        # Step 5: Create charts
        chart_filename = self.create_portfolio_charts()
        
        # Step 6: Generate email report
        html_content = self.generate_email_report(alerts, chart_filename)
        
        # Step 7: Send email
        email_sent = self.send_email_report(html_content, chart_filename)
        
        # Step 8: Update Excel
        excel_updated = self.update_portfolio_excel(output_excel_path)
        
        # Step 9: Summary
        print("=" * 50)
        print("📊 Daily Portfolio Tracker Summary:")
        print(f"   ✅ Portfolio loaded: {len(self.portfolio_data)} stocks")
        print(f"   ✅ Prices fetched: {len(self.current_prices)} stocks")
        print(f"   ✅ Alerts found: {len(alerts)} stocks")
        print(f"   ✅ Email sent: {'Yes' if email_sent else 'No'}")
        print(f"   ✅ Excel updated: {'Yes' if excel_updated else 'No'}")
        print(f"   📈 Total P&L: ₹{self.daily_report['total_pl']:,.2f} ({self.daily_report['total_pl_percentage']:+.2f}%)")
        
        return True

def create_sample_portfolio():
    """Create a sample portfolio Excel file for testing"""
    sample_portfolio = pd.DataFrame({
        'Stock_Symbol': PORTFOLIO_LIST,
        'Company_Name': ['Tata Motors', 'Tata Steel', 'Infosys', 'LIC', 'Vedanta', 'Exide Industries', 
                         'Tata Power', 'Trident', 'ONGC', 'Tata Chemicals', 'NTPC', 'IRCTC', 'IEX', 'HCL Tech'],
        'Purchase_Date': ['2024-01-15', '2024-01-20', '2024-02-01', '2024-02-10', '2024-02-15', '2024-03-01',
                          '2024-03-10', '2024-03-15', '2024-03-20', '2024-04-01', '2024-04-10', '2024-04-15',
                          '2024-04-20', '2024-05-01'],
        'Purchase_Price': [800, 120, 1500, 800, 250, 300, 200, 50, 150, 1000, 200, 800, 150, 1200],
        'Quantity': [100, 500, 50, 100, 200, 150, 250, 1000, 300, 50, 200, 50, 200, 50]
    })
    
    # Calculate total investment
    sample_portfolio['Total_Investment'] = sample_portfolio['Purchase_Price'] * sample_portfolio['Quantity']
    
    # Save to Excel
    sample_portfolio.to_excel('sample_portfolio.xlsx', index=False)
    print("✅ Sample portfolio created: 'sample_portfolio.xlsx'")
    print(f"💰 Total Investment: ₹{sample_portfolio['Total_Investment'].sum():,.2f}")
    
    return sample_portfolio

def main():
    """Main function to run the portfolio tracker"""
    print("🚀 PORTFOLIO TRACKER SYSTEM")
    print("=" * 50)
    
    # Check if sample portfolio exists, if not create it
    if not os.path.exists('sample_portfolio.xlsx'):
        print("📋 Creating sample portfolio...")
        create_sample_portfolio()
    
    # Initialize tracker
    tracker = PortfolioTracker()
    
    # Run daily tracker
    success = tracker.run_daily_tracker('sample_portfolio.xlsx', 'updated_portfolio.xlsx')
    
    if success:
        print("\n🎉 Daily portfolio tracking completed successfully!")
        print("📧 Check your email for the daily report")
        print("📁 Check 'updated_portfolio.xlsx' for updated data")
    else:
        print("\n❌ Daily portfolio tracking failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
