# 🚀 Automated Portfolio Tracker - Setup Guide

## Overview
This system automatically tracks your portfolio performance daily and sends comprehensive email reports with:
- 📊 Daily portfolio performance tracking
- 📈 Real-time price updates via Yahoo Finance
- 🚨 P&L alerts for stocks outside ±5% threshold
- 📧 Automated daily email reports with charts
- 📁 Excel file updates and performance history
- 📊 Portfolio visualization charts

## 🛠️ Installation & Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Update Email Credentials
Edit `portfolio_tracker.py` and update these lines:
```python
EMAIL_SENDER = "your_email@gmail.com"      # Your Gmail address
EMAIL_PASSWORD = "your_app_password"        # Your Gmail App Password
EMAIL_RECEIVER = "your_email@gmail.com"     # Where to send reports
```

**⚠️ Important:** You need a Gmail App Password, not your regular password:
1. Go to Google Account Settings
2. Enable 2-Factor Authentication
3. Generate App Password for "Mail"
4. Use that 16-character password

### 3. Prepare Your Portfolio Excel File
The system expects an Excel file with these columns:
- `Stock_Symbol` - NSE stock symbols (e.g., TATAMOTORS, INFY)
- `Company_Name` - Full company name
- `Purchase_Date` - When you bought (YYYY-MM-DD format)
- `Purchase_Price` - Price per share when bought
- `Quantity` - Number of shares purchased

**Example:**
| Stock_Symbol | Company_Name | Purchase_Date | Purchase_Price | Quantity |
|--------------|--------------|---------------|----------------|----------|
| TATAMOTORS   | Tata Motors  | 2024-01-15    | 800            | 100      |
| INFY         | Infosys      | 2024-02-01    | 1500           | 50       |

## 🧪 Testing the System

### 1. Test Run
```bash
python portfolio_tracker.py
```

This will:
- Create a sample portfolio if none exists
- Fetch current market prices
- Calculate performance metrics
- Generate charts
- Send email report
- Update Excel files

### 2. Check Outputs
- `sample_portfolio.xlsx` - Your portfolio template
- `updated_portfolio.xlsx` - Updated with current prices
- `portfolio_data/portfolio_data_YYYYMMDD.json` - Daily price snapshots
- `portfolio_charts/portfolio_chart_YYYYMMDD.png` - Daily charts
- Email report in your inbox

## 🚀 Setting Up Daily Automation

### Option A: Windows Task Scheduler
1. Open "Task Scheduler" (search in Start menu)
2. Click "Create Basic Task"
3. Name: "Portfolio Tracker Daily"
4. Trigger: Daily
5. Start time: 5:00 AM
6. Action: Start a program
7. Program: `python`
8. Arguments: `portfolio_tracker.py`
9. Start in: `C:\path\to\your\portfolio\folder`

### Option B: Linux/Mac Cron Job
1. Open terminal
2. Run: `crontab -e`
3. Add this line:
```bash
0 5 * * * cd /path/to/portfolio && python portfolio_tracker.py
```
4. Save and exit

### Option C: Cloud Platforms
- **AWS Lambda + EventBridge**: Schedule daily execution
- **Google Cloud Functions + Cloud Scheduler**: Automated daily runs
- **Azure Functions + Logic Apps**: Scheduled execution

## 📊 Understanding the Reports

### Daily Email Report Includes:
1. **Portfolio Summary**
   - Total Investment
   - Current Value
   - Total P&L (₹ and %)

2. **Individual Stock Performance**
   - Current price for each stock
   - Individual P&L (₹ and %)

3. **Alerts**
   - Stocks with P&L outside ±5% threshold
   - Color-coded (green for profit, red for loss)

4. **Portfolio Charts**
   - Pie chart showing allocation by value
   - Bar chart showing P&L by stock

### Excel Files Generated:
1. **Portfolio Sheet**: Current portfolio with live prices
2. **Daily Summary**: Today's performance snapshot
3. **Performance History**: Historical daily performance data

## 🔧 Troubleshooting

### Common Issues:

1. **Email Not Sending**
   - Check Gmail App Password is correct
   - Ensure 2FA is enabled on Gmail
   - Check internet connection

2. **Prices Not Fetching**
   - Verify stock symbols are correct NSE symbols
   - Check internet connection
   - Yahoo Finance API might be temporarily down

3. **Excel File Errors**
   - Ensure Excel file is not open when script runs
   - Check file paths are correct
   - Verify required columns exist

4. **Charts Not Generating**
   - Install matplotlib and seaborn: `pip install matplotlib seaborn`
   - Check if you have write permissions in the directory

### Debug Mode:
Add this line at the top of the script for detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Customization Options

### 1. Change Alert Threshold
```python
ALERT_THRESHOLD = 10.0  # Alert for P&L outside ±10%
```

### 2. Modify Report Time
```python
REPORT_TIME = "06:00"  # 6:00 AM instead of 5:00 AM
```

### 3. Add More Stocks
```python
PORTFOLIO_LIST = ['TATAMOTORS', 'INFY', 'RELIANCE', 'TCS', 'HDFC']
```

### 4. Custom Email Template
Modify the `generate_email_report()` method to change the email format.

## 🔒 Security Considerations

1. **Email Credentials**: Never commit your email password to version control
2. **File Permissions**: Ensure portfolio Excel files are not publicly accessible
3. **API Limits**: Yahoo Finance has rate limits; don't run too frequently
4. **Data Privacy**: Portfolio data contains sensitive financial information

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Test with the sample portfolio first
4. Check console output for error messages

## 🎯 Next Steps

1. **Test the system** with sample data
2. **Update with your actual portfolio** data
3. **Set up daily automation** using your preferred method
4. **Monitor daily reports** and adjust as needed
5. **Customize alerts** and thresholds based on your preferences

---

**Happy Portfolio Tracking! 📊📈**
