from flask import Flask
import redis
import os

app = Flask(__name__)

redis_host = os.environ.get("REDIS_HOST", "127.0.0.1")

cache = redis.Redis(host=redis_host,port=6379,socket_connect_timeout=2,socket_timeout=2)

@app.route("/visits")
def visits():
    
    try:
        count = cache.incr("visits")  
        return f"Visits: {count}"
    except redis.exceptions.RedisError:
        return "unavailable",503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
