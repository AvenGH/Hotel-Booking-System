import smtplib
from email.message import EmailMessage


def send_email(file_name, email, sender, receiver_email, subject, data, subtype, host_password):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender 
    msg['To'] = receiver_email

    msg.set_content(data)

    with open(file_name, "rb") as f:
        file_data = f.read()
        file_name = f.name
        msg.add_attachment(file_data, maintype="application", subtype="txt", filename=file_name.split("\\")[-1])

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(email, host_password)
        server.send_message(msg)

    print(f"Successfully sent an email to {receiver_email}!!!")

'''

'''