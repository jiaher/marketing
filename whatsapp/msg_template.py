# msg_template.py

def get_message_template():
    """
    Returns the template for client messages. Use Python's format string syntax
    with the following variables:
    - name: Client's name
    - investment_amount: Original investment amount
    - account_value: Current account value
    - profit_loss: Calculated profit or loss amount
    - profit_loss_percentage: Percentage gain or loss
    
    Returns:
        str: Message template with placeholders for client data
    """
    return """Dear {name},

Here's your portfolio update:
Investment Amount: ₹{investment_amount:,.2f}
Current Value: ₹{account_value:,.2f}
Profit/Loss: ₹{profit_loss:,.2f} ({profit_loss_percentage:.2f}%)

Please contact us if you have any questions.

Best regards,
Your Portfolio Manager"""

# Optional: Add additional message templates for different scenarios
def get_high_performance_template():
    """Template for clients with significant gains (e.g., >10%)"""
    return """Dear {name},

Excellent news! Your portfolio has shown strong performance:
Initial Investment: ₹{investment_amount:,.2f}
Current Value: ₹{account_value:,.2f}
Total Gain: ₹{profit_loss:,.2f} ({profit_loss_percentage:.2f}%)

Would you like to schedule a call to discuss optimization strategies?

Best regards,
Your Portfolio Manager"""

def get_low_performance_template():
    """Template for clients with losses (e.g., <0%)"""
    return """Dear {name},

Important Portfolio Update:
Initial Investment: ₹{investment_amount:,.2f}
Current Value: ₹{account_value:,.2f}
Current Change: ₹{profit_loss:,.2f} ({profit_loss_percentage:.2f}%)

I would like to schedule a review meeting to discuss market conditions and adjustment strategies.

Best regards,
Your Portfolio Manager"""