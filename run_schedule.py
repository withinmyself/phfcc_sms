from schedule_handler import AlertScheduler
time_obj = AlertScheduler('monday')
time_obj.message_loop()
time_obj.change_second()
