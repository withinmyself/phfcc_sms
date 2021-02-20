import redis
import vonage




redis_client = redis.Redis()

key = str(redis_client.get("VONAGE_KEY").decode("utf-8"))
secret = str(redis_client.get("VONAGE_SECRET").decode("utf-8"))
number = int(redis_client.get("VONAGE_NUMBER").decode("utf-8"))

client = vonage.Client(key=key, secret=secret)
sms = vonage.Sms(client)
