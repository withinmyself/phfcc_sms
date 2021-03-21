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
                if self._covid_message.auto_send:
                    self.send_sms(str(member.phone_number), self._covid_message.message)
                if self._weather_message.auto_send:
                    self.send_sms(str(member.phone_number), self._weather_message.message)
                if self._meetings.message.auto_send:
                    self.send_sms(str(member.phone_number), self._meetings.message)
                if self._prayer_chain.auto_send:
                    self.send_sms(str(member.phone_number), self._prayer_chain.message)
                return 'Sent all messages that are marked for automatic weekly alerts.'
            elif message_type == 'Covid':
                self.send_sms(str(member.phone_number), self._covid_message.message)
                return 'Sent Covid message.'
            elif message_type == 'Weather':
                self.send_sms(str(member.phone_number), self._weather_message.message)
                return 'Sent Weather message'
            elif message_type == 'Meetings':
                self.send_sms(str(member.phone_number), self._meetings.message)
                return 'Sent Meetings message'
            elif message_type == 'Prayer Chain':
                self.send_sms(str(member.phone_number), self._prayer_chain.message)
                return 'Sent Prayer Chain message'
            else:
                return 'Message Type Not Found.'
        return 'No messages sent', 404

    def send_sms(self, number, msg):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(self._username, self._password)
            from_mail = 'PHFCC'
            tmobile = f'{number}@tmomail.net'
            sprint = f'{number}@messaging.sprintpcs.com'
            verizon = f'{number}@vtext.com'
            usscellular = f'{number}@email.uscc.net'
            virgin = f'{number}@vmobl.com'
            att = f'{number}@txt.att.net'
            body = msg
            message = ("From: %s\r\n" % from_mail + "To: %s\r\n" % to + "Subject: %s\r\n" % self.message_type + "\r\n" + body)

            try:
                smtp.sendmail(from_mail, sprint, message)
            except smtplib.SMTPRecipientsRefused:
                print(f'In exception. {e}')
            return '200'


