import pandas as pd
import pywhatkit
import openpyxl
import time

from datetime import datetime, timedelta
from msg_template import (
    get_message_template,
    get_high_performance_template,
    get_low_performance_template,
    get_emoji_for_performance,
    set_header,
    set_body,
    set_footer)   

def read_client_data(file_path):
    """
    Read client data from Excel file.
    Returns a pandas DataFrame with client information.
    """
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Verify required columns exist
        required_columns = ['clientIdentityNumber', 
                            'clientNickname', 
                            'clientAccountStatus', 
                            'clientInvestment', 
                            'clientSourceOfFunds', 
                            'clientContactPhone', 
                            'portfolioValue0', 
                            'snapshotDate0', 
                            'delta', 
                            'snapshotDate-1']
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
    
    # phone = ''.join(filter(str.isdigit, str(phone))) // uncomment if all numbers are +65 Singapore numbers
    phone = str(phone)
    
    # Add country code if not present
    if not phone.startswith('+'):
        phone = '+65' + phone  # Change country code as needed
    
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

def construct_whatsapp_messages(df):
    """
    Construct a dictionary of WhatsApp messages to clients with personalized information.
    key: phone number
    value: {header, body, footer}
    """
    
    messages_dict = {}
    
    for index, row in df.iterrows():
        
        try:
            
            status = row['clientAccountStatus']
            print(status)
            # Do not send messages to inactive accounts i.e. status = 0 or negative
            if status > 0:
                #key = row['clientIdentityNumber']
                key = int(row['clientContactPhone'])
                #print(int(key))
                name = row['clientNickname']
                source=row['clientSourceOfFunds']
                currency=row['clientInvestmentCurrency']
                investment_amount=row['clientInvestment']
                account_value=row['portfolioValue0']
                last_account_value=row['portfolioValue-1']
                snapshot_date=row['snapshotDate0'].strftime('%d %b %Y')
                last_snapshot_date=row['snapshotDate-1'].strftime('%d %b %Y')
                
                # Calculate profit/loss
                profit_loss = account_value - last_account_value
                profit_loss_percentage = row['delta'] * 100
                
                # Get appropriate emoji for the performance
                performance_emoji = get_emoji_for_performance(profit_loss_percentage)
                
                # Select and format appropriate message template
                #message_template = select_message_template(profit_loss_percentage)
                
                if key not in messages_dict:
                    messages_dict[key] = {'header': '', 'body': [] , 'footer':''} #[]  # Initialize message dictionary
                
                messages_dict[key]['header'] = set_header().format(name=name)
                
                message = set_body().format(
                    source=source,
                    currency=currency,
                    investment_amount=investment_amount,
                    snapshot_date=snapshot_date,
                    account_value=account_value,
                    profit_loss=profit_loss,
                    profit_loss_percentage=profit_loss_percentage,
                    last_snapshot_date=last_snapshot_date,
                    emoji=performance_emoji
                    
                )
                
                messages_arr = messages_dict[key]['body']
                messages_arr.append(message)
                
                messages_dict[key]['footer'] = set_footer()
                
        except Exception as e:
            print(f"Error constructing message to {row['clientLegalName']}: {e}")

    print(messages_dict)
    return messages_dict
    
def send_whatsapp_messages(messages_dict, delay_minutes=2):
    """
    Send WhatsApp messages to clients with personalized information.
    Includes delay between messages to prevent blocking.
    """
    #current_time = datetime.now()
    
    
    for key, message_parts in messages_dict.items():
        
        
        # Format phone number
        phone_number = format_phone_number(key)
                
        message = message_parts['header'] + ''.join(message_parts['body']) + message_parts['footer']       
        try:
                # Send message using pywhatkit
                pywhatkit.sendwhatmsg_instantly(phone_number, message,30, False, 3)
                
        except Exception as e:
                print(f"Error sending message to {phone_number}: {e}")
    
def main():
    """
    Main function to execute the client messaging system.
    """
    # File path to your Excel file
    #excel_file = "test.xlsx"
    excel_file = "data-jul-2025.xlsx"
    
    # Read client data
    client_data = read_client_data(excel_file)
    
    if client_data is not None:
        print("Starting to send messages...")
        construct_whatsapp_messages(client_data)
        send_whatsapp_messages(construct_whatsapp_messages(client_data))       
        print("Message scheduling completed!")
    else:
        print("Failed to read client data. Please check your Excel file.")

if __name__ == "__main__":
    main()