import os
import sys
import smtplib
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def clear_screen():
    """Clears the terminal screen in Linux."""
    os.system('clear')

def display_banner():
    """Displays the REX TOOL ASCII art."""
    banner = """
██████╗ ███████╗██╗  ██╗    ████████╗ ██████╗  ██████╗ ██╗     
██╔══██╗██╔════╝╚██╗██╔╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
██████╔╝█████╗   ╚███╔╝        ██║   ██║   ██║██║   ██║██║     
██╔══██╗██╔══╝   ██╔██╗        ██║   ██║   ██║██║   ██║██║     
██║  ██║███████╗██╔╝ ██╗       ██║   ╚██████╔╝╚██████╔╝███████╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
    """
    print(banner)
    print("===============================================================")
    print("                      System Utilities Menu                    ")
    print("===============================================================\n")

def email_sender():
    """Function to send emails via SMTP."""
    clear_screen()
    display_banner()
    print("[+] --- EMAIL SENDER OPTION --- [+]\n")

    # Get SMTP provider settings
    print("Select SMTP Provider:")
    print("1. Gmail (smtp.gmail.com)")
    print("2. Outlook/Hotmail (smtp.office365.com)")
    print("3. Yahoo (smtp.mail.yahoo.com)")
    print("4. Custom SMTP")
    
    provider_choice = input("\nChoose an option [1-4]: ").strip()
    
    if provider_choice == '1':
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
    elif provider_choice == '2':
        smtp_server = "smtp.office365.com"
        smtp_port = 587
    elif provider_choice == '3':
        smtp_server = "smtp.mail.yahoo.com"
        smtp_port = 587
    elif provider_choice == '4':
        smtp_server = input("Enter SMTP Server Address: ").strip()
        try:
            smtp_port = int(input("Enter SMTP Port (usually 587 or 465): ").strip())
        except ValueError:
            print("Invalid port number. Defaulting to 587.")
            smtp_port = 587
    else:
        print("Invalid choice. Returning to menu.")
        input("\nPress Enter to return...")
        return

    # Gather credentials and email details
    sender_email = input("\nEnter your email address: ").strip()
    # Using getpass so the password does not display on screen while typing
    sender_password = getpass.getpass("Enter your password (or App Password): ")
    
    recipient_email = input("Enter recipient email address: ").strip()
    subject = input("Enter email subject: ").strip()
    message_body = input("Enter message content: ")
    
    try:
        count = int(input("How many times do you want to send this email?: ").strip())
        if count <= 0:
            print("Count must be greater than 0.")
            input("\nPress Enter to return...")
            return
    except ValueError:
        print("Invalid number entered. Aborting.")
        input("\nPress Enter to return...")
        return

    print("\n[+] Attempting to send email(s)...")
    
    # Establish connection and send
    try:
        # Use SMTP_SSL for port 465, standard SMTP + STARTTLS for 587
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            
        server.login(sender_email, sender_password)
        
        for i in range(1, count + 1):
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f"{subject} (Copy #{i})" if count > 1 else subject
            msg.attach(MIMEText(message_body, 'plain'))
            
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"[{i}/{count}] Email sent successfully to {recipient_email}")
            
        server.quit()
        print("\n[+] All tasks completed.")
        
    except Exception as e:
        print(f"\n[-] An error occurred: {e}")
        print("Verify your credentials, network connection, and SMTP settings.")
        
    input("\nPress Enter to return to the main menu...")

def main_menu():
    while True:
        clear_screen()
        display_banner()
        print("1. Email Sender")
        print("2. Phone Lookup")
        print("3. IP Lookup")
        print("4. Email Lookup")
        print("5. Exit")
        
        choice = input("\nSelect an option [1-5]: ").strip()
        
        if choice == '1':
            email_sender()
        elif choice in ['2', '3', '4']:
            clear_screen()
            display_banner()
            print(f"Option {choice} is currently under construction.")
            input("\nPress Enter to return to the menu...")
        elif choice == '5':
            print("\nExiting REX TOOL. Goodbye.")
            sys.exit()
        else:
            print("\nInvalid choice. Please choose between 1 and 5.")
            input("\nPress Enter to try again...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nSession terminated by user.")
        sys.exit()
