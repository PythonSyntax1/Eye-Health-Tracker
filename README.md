# Eye-Health-Tracker

Python application that tracks a user's blink frequency through their web-cam, and sends an email every hour that details the user's blink frequency.
  - Built with OpenCV, combined with DLib's facial landmark libraries

Notes:
  - Emailing feature can be enabled through modifying code. This is to prevent security worries.
  - To enable emailing feature, enter report.py and make the follow edits:
  
     ```python
       #Enter email server here
      server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Enter email username and password here
        server.login("email", "pass")
        healthMessage = self.generateHealthMessage()
     ```
     
     ```python
     #Enter sending email, and recieving email respectively. 
     server.sendmail("email", "email", Message)
     ```
