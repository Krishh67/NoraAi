import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sender and receiver details
sender_email = "krishp4216@gmail.com"
receiver_email = "krishp0321@gmail.com"
password = "amoz ghwz lubi khlm"   # ⚠️ Not your Gmail password, use App Password

# Create the email
subject = "GDG HackX Registration Successful"
body = "Hi Krish,\n\nYour registration for GDG HackX is confirmed! 🎉\n\nSee you at the event.\n\n- GDG Team"

msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

try:
    # Connect to Gmail SMTP
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # Secure connection
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    print("✅ Email sent successfully!")
    server.quit()
except Exception as e:
    print("❌ Error:", e)
