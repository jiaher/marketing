import pandas as pd
import pywhatkit
import time
from datetime import datetime, timedelta
from message_template import (
    get_message_template,
    get_high_performance_template,
    get_low_performance_template
)

def read_client_data(file_path):
    """
    Read client data from Excel file.
    Returns a pandas DataFrame with client information.
    """
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Verify required columns exist
        required_columns = ['name', 'phone_number', 'investment_amount', 'account_value']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
            
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def format_phone_number(phone):
    """
    Format phone number to required format (+CountryCode followed by number)
    Example: converts "1234567890" to "+911234567890" for India
    """
    # Remove any non-numeric characters
    phone = ''.join(filter(str.isdigit, str(phone)))
    
    # Add country code if not present
    if not phone.startswith('+'):
        phone = '+91' + phone  # Change country code as needed
    
    return phone

def select_message_template(profit_loss_percentage):
    """
    Select appropriate message template based on portfolio performance.
    
    Args:
        profit_loss_percentage (float): The percentage gain or loss
    
    Returns:
        function: The appropriate template function
    """
    if profit_loss_percentage >= 10:
        return get_high_performance_template()
    elif profit_loss_percentage < 0:
        return get_low_performance_template()
    else:
        return get_message_template()

def send_whatsapp_messages(df, delay_minutes=2):
    """
    Send WhatsApp messages to clients with personalized information.
    Includes delay between messages to prevent blocking.
    """
    current_time = datetime.now()
    
    for index, row in df.iterrows():
        try:
            # Format phone number
            phone_number = format_phone_number(row['phone_number'])
            
            # Calculate profit/loss
            profit_loss = row['account_value'] - row['investment_amount']
            profit_loss_percentage = (profit_loss / row['investment_amount']) * 100
            
            # Select and format appropriate message template
            message_template = select_message_template(profit_loss_percentage)
            message = message_template.format(
                name=row['name'],
                investment_amount=row['investment_amount'],
                account_value=row['account_value'],
                profit_loss=profit_loss,
                profit_loss_percentage=profit_loss_percentage
            )
            
            # Calculate send time (current time + delay for each iteration)
            send_time = current_time + timedelta(minutes=delay_minutes * index)
            
            # Send message using pywhatkit
            pywhatkit.sendwhatmsg(
                phone_number,
                message,
                send_time.hour,
                send_time.minute,
                wait_time=20,
                tab_close=True
            )
            
            print(f"Message scheduled for {row['name']} at {send_time.strftime('%H:%M')}")
            
        except Exception as e:
            print(f"Error sending message to {row['name']}: {e}")

def main():
    """
    Main function to execute the client messaging system.
    """
    # File path to your Excel file
    excel_file = "client_portfolio.xlsx"
    
    # Read client data
    client_data = read_client_data(excel_file)
    
    if client_data is not None:
        print("Starting to send messages...")
        send_whatsapp_messages(client_data)
        print("Message scheduling completed!")
    else:
        print("Failed to read client data. Please check your Excel file.")

if __name__ == "__main__":
    main()