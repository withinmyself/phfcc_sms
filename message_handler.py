import smtplib
from app import Members, Messages
import redis


class SendSMS():
    """
    """
    def __init__(self):
        self._redis_client = redis.Redis()
        self._members_to_text = Members.query.all()
        self._covid_message = Messages.query.filter_by(message_type='Covid').first()
        self._weather_message = Messages.query.filter_by(message_type='Weather').first()
        self._meetings = Messages.query.filter_by(message_type='Meetings').first()
        self._prayer_chain = Messages.query.filter_by(message_type='Prayer Chain').first()
        self._username = str(self._redis_client.get('SMS_USER').decode('utf-8'))
        self._password = str(self._redis_client.get('SMS_PASS').decode('utf-8'))


    def send_sms_all(self, message_type):
        members_to_text = Members.query.all()
        self.message_type = message_type
        for member in members_to_text:
            if message_type == 'ALL':
                self.send_sms(str(member.phone_number), self._covid_message.message)
                self.send_sms(str(member.phone_number), self._weather_message.message)
                self.send_sms(str(member.phone_number), self._meetings.message)
                self.send_sms(str(member.phone_number), self._prayer_chain.message)
                break
                return 'Sent'
            elif message_type == 'Covid':
                self.send_sms(str(member.phone_number), self._covid_message.message)
                return 'Sent'
            elif message_type == 'Weather':
                self.send_sms(str(member.phone_number), self._weather_message.message)
                return 'Sent'
            elif message_type == 'Meetings':
                self.send_sms(str(member.phone_number), self._meetings.message)
                return 'Sent'
            elif message_type == 'Prayer Chain':
                self.send_sms(str(member.phone_number), self._prayer_chain.message)
                return 'Sent'
            else:
                return 'Message Type Not Found.'
        return '200'



    def send_sms(self, number, msg):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(self._username, self._password)
            from_mail = 'PHFCC'
            to = f'{number}@tmomail.net'
            body = msg
            message = ("From: %s\r\n" % from_mail + "To: %s\r\n" % to + "Subject: %s\r\n" % self.message_type + "\r\n" + body)

            try:
                smtp.sendmail(from_mail, to, message)
            except smtplib.SMTPRecipientsRefused as e:
                print(e)
            return '200'


