# msg_template.py

TXT_GREETING = "happy new year to u!\n"
TXT_OPENING = "Having concluded 2H 2024, here is a quick update on your investments with me:\n"
TXT_FOOTER = "\n\nRefer to my commentary for a recap of 2H 2024 here: https://bit.ly/prestigeraffles2H2024\n\nFeel free to reach out for a quick update and explore any top-up.\n\nLastly, appreciate if u will pass my name on to benefit people around u with my expertise."
TXT_SIGNATURE = "\n\nChung Tze,\nManulife Financial Advisers"


def get_emoji_for_performance(percentage):
    """
    Returns appropriate emojis based on portfolio performance.
    This function helps maintain consistent emoji usage across messages.
    """
    if percentage >= 10:
        return "🚀 📈"  # Rocket and upward trend
    elif percentage >= 0:
        return "📈"     # Upward trend
    elif percentage >= -10:
        return "📉"     # Downward trend
    else:
        return "📉 ⚠️"  # Downward trend and warning

def get_message_template():
    """
    Returns the standard template for client messages with emoji support.
    Uses Unicode emojis for guaranteed compatibility.
    """
    return """Dear {name}

📊 Portfolio Update:
Investment Amount: ${investment_amount:,.2f}
Current Value: ${account_value:,.2f}
Performance: {emoji} ${profit_loss:+,.2f} ({profit_loss_percentage:+.2f}%)

Please reach out if you have any questions! 💬

Best regards,
Your Portfolio Manager ✨"""

def get_high_performance_template():
    """Template for clients with significant gains"""
    return """Dear {name} 👋

🌟 Outstanding Portfolio Performance! 🌟

Investment Amount: ${investment_amount:,.2f}
Current Value: ${account_value:,.2f}
Remarkable Growth: {emoji} ${profit_loss:+,.2f} ({profit_loss_percentage:+.2f}%)

Would you like to schedule a call to discuss optimization strategies? 📞

Best regards,
Your Portfolio Manager 🚀"""

def get_low_performance_template():
    """Template for clients with losses"""
    return """Dear {name} 👋

⚠️ Important Portfolio Update ⚠️

Investment Amount: ${investment_amount:,.2f}
Current Value: ${account_value:,.2f}
Current Change: {emoji} ${profit_loss:+,.2f} ({profit_loss_percentage:+.2f}%)

Let's schedule a review meeting to discuss market conditions and adjustment strategies 🤝

Best regards,
Your Portfolio Manager 📊"""

def set_body():
    """
    Each entry represents an account update. If a customer has N accounts, then expect N entries in a single Whatsapp message.
    
    Returns:
        str: The full message entry
    """
    return """
{source} invested {currency} {investment_amount:,.2f}
Portfolio value as of {snapshot_date}: {currency} {account_value:,.2f} ({profit_loss_percentage:+.2f}% from {last_snapshot_date})

--------------------------"""

def set_header():
    """
    Returns:
        str: The header message
    """
    return """Dear {name}, """ +  TXT_GREETING + TXT_OPENING


def set_footer():
    """
    Returns:
        str: The footer message
    """
    return TXT_FOOTER + TXT_SIGNATURE