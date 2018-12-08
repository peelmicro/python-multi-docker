import redis
import os
import time

def fib(index):
  if (index < 2): 
    return 1
  return fib(index - 1) + fib(index - 2)

def main():
  redisHost = os.getenv("REDIS_HOST", "localhost")
  redisPort = int(os.getenv("REDIS_PORT", "6379"))
  try:
    redisSubscription = redis.Redis(host=redisHost, port=redisPort, db=0)
    publishSubscription = redisSubscription.pubsub()
    publishSubscription.subscribe('message')
    while True:
      message = publishSubscription.get_message(ignore_subscribe_messages=True)
      if (message):
        data = message["data"]
        setKey = "values"
        redisKey = setKey + data.decode()
        redisSet = redis.Redis(host=redisHost, port=redisPort, db=0)
        redisSet.set(redisKey, str(fib(int(data.decode()))))
        redisSet.sadd(setKey, redisKey)
      time.sleep(1)
  except Exception as e:
    print(str(e))

if __name__=="__main__":
  main()
