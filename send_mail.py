# Python code to illustrate Sending mail from  
# your Gmail account  
import smtplib

'''https://myaccount.google.com/lesssecureapps'''
def send_mail_gmail(message,recivermail):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("raajrajnish@gmail.com", "lr201203m")
    # message to be sent
    message = message
    # sending the mail
    s.sendmail("raajrajnish@gmail.com", recivermail, message)
    # terminating the session
    s.quit()
    print('mail send')

#send_mail_gmail('message','shukladevanshu1989@gmail.com')