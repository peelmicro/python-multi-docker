from flask import Flask, jsonify, request, make_response
import redis
import os
import psycopg2

app = Flask(__name__)
# global Redis
redisHost = os.getenv("REDIS_HOST", "localhost")
redisPort = int(os.getenv("REDIS_PORT", "6379"))
setKey = "values"

# Postgres
pgUser = os.getenv("PGUSER")
pgHost = os.getenv("PGHOST")
pgDatabase = os.getenv("PGDATABASE")
pgPassword = os.getenv("PGPASSWORD")
pgPort = int(os.getenv("PGPORT","5432"))
try:
  pgConnection = psycopg2.connect(host=pgHost,database=pgDatabase, user=pgUser, password=pgPassword, port=pgPort)
  pgCursor = pgConnection.cursor()
  pgCursor.execute('CREATE TABLE IF NOT EXISTS values (number INT)')
  pgCursor.close()
except Exception as e:
  print(str(e))  

@app.route('/')
def hello():
    return 'Hi'

@app.route('/values/all')
def getAll():
  values = []
  pgCursor = pgConnection.cursor()
  pgCursor.execute('SELECT number from values')
  for record in pgCursor.fetchall():
    result = {
      "number": record[0]
    }
    values.append(result)
  pgCursor.close()
  return jsonify(values)

@app.route('/values/current')
def getCurrent():
  redisGet = redis.Redis(host=redisHost, port=redisPort, db=0)
  result = {}
  for item in redisGet.smembers(setKey):
    value = redisGet.get(item)
    key = item.decode().replace(setKey, "")
    result[key] = value.decode()
  return jsonify(result)
    
@app.route('/values', methods = ['POST'])
def post():
  postedData = request.get_json()
  validIndex = True
  number = 0

  if "index" not in postedData:
    validIndex = False
  else:
    index = postedData["index"]
    try:
      number = int(index)
      if (number > 40):
        validIndex = False
    except:
      validIndex = False

  if (validIndex == False):
    response = { 
      "working": False,
      "message": "Invalid Index!"
    }
    return make_response(jsonify(response), 422)

  pgCursor = pgConnection.cursor()
  pgCursor.execute('INSERT INTO values(number) VALUES(%s)', [number])
  pgCursor.close()

  redisKey = setKey + index
  redisSet = redis.Redis(host=redisHost, port=redisPort, db=0)
  redisSet.set(redisKey, "Nothing yet!")
  redisSet.sadd(setKey, redisKey)
  redisSet.publish("message", index)

  response = { 
    "working": True
  }
  return jsonify(response)

if __name__=="__main__":
  app.run(host='0.0.0.0')