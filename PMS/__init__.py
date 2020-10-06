import africastalking
import os

username = os.getenv('user_name', 'sandbox')
api_key = os.getenv('api_key', 'bf66183d227f2321feffa3e876fde78f1dae245aa84dae4754841c515759d142')

africastalking.initialize(username, api_key)
sms = africastalking.SMS

