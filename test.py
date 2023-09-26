import json
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load the JSON data from the file
with open('trident_secret.json', 'r') as json_file:
   data = json.load(json_file)

# Get all cluster API URLs
cluster_api_urls = [api for api in data.keys()]

# SMTP server configuration
smtp_server_host = '10.56.131.8'  # Replace with your SMTP server's host
smtp_server_port = 25  # Replace with your SMTP server's port

# Connect to the SMTP server
smtp_server = smtplib.SMTP(smtp_server_host, smtp_server_port)

# Email configuration
from_email = 'alert@trident.com'
recipient_email = 'test@email.com'

last_updated_str = "2023-08-10:00:00:00"

for cluster_api_url in cluster_api_urls:
    last_updated_str = data.get(cluster_api_url, {}).get("last_updated")
    
    if last_updated_str:
        last_updated = datetime.datetime.strptime(last_updated_str, "%Y-%m-%dT%H:%M:%S.%f")
        current_date = datetime.datetime.now()
    
        # Calculate the difference in days
        date_difference = (current_date - last_updated).days
        #print(date_difference)
    
        # Check if the difference is less than 5 days
        if date_difference > 70:
            # Create the email message
            subject = f"Your Trident User Password for Cluster {cluster_api_url} is about to Expire!!"
            message = f"Your Trident User Password for Cluster {cluster_api_url} is about to Expire in {date_difference} Days!!."
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))
    
            # Send the email
            try:
                text = msg.as_string()
                smtp_server.sendmail(from_email, recipient_email, text)
                print(f"Email sent for {cluster_api_url}.")
            except Exception as e:
                print(f"Failed to send email for {cluster_api_url}: {str(e)}")
        else:
            print(f"No email sent for {cluster_api_url} as the difference in days is ({date_difference}) .")
    else:
        print(f"Cluster API URL {cluster_api_url} not found in the JSON data.")

# Quit the SMTP server
smtp_server.quit()
