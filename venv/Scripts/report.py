import smtplib


class Report:

    def __init__(self, result, time):
        self.time = time
        self.result = result
        self.rate = None

    def sendMail(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Enter email username and password here
        server.login("user", "pass")
        healthMessage = self.generateHealthMessage()

        # Email message
        Message = "You blinked " + self.result + " times in " + self.time + "This is a rate of " + self.rate + "blinks per minute. " + healthMessage
        server.sendmail(self.email, self.email, Message)

    def generateHealthMessage(self):

        # Returns a message based on the amount of times you blinked per minute.
        rate = self.result / self.time
        if rate > 15:
            return "This is a healthy pace. Keep it up!"
        elif 15 > rate > 10:
            return "You are blinking less than average. Please give your eyes a rest and try to blink more!"
        else:
            return "You are blinking at a very low rate! Please give your eyes a rest and try to blink more! If you " \
                   "believe this is a mistake, please try recalibrating the system "

