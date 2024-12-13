from flask import Flask, request, jsonify
import redis
import time
import threading

app = Flask(__name__)

# Redis connection
redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

# Rate limiting configuration
REQUEST_LIMIT = 10
TIME_WINDOW = 60  

def get_client_identifier():
    """
    Get the client's IP address as the identifier.
    """
    client_ip = request.remote_addr  # Client's IP address
    print(client_ip)
    return client_ip

def get_request_count(client_identifier):
    """
    Get the current number of requests made by the client in the current time window.
    """
    request_key = f"request_count:{client_identifier}"
    request_count = redis_client.get(request_key)
    if request_count is None:
        # If the key doesn't exist, initialize it with 1 and set expiration time (TIME_WINDOW)
        redis_client.setex(request_key, TIME_WINDOW, 1)
        return 1
    return int(request_count)

def increment_request_count(client_identifier):
    """
    Increment the number of requests made by the client in the current time window.
    """
    request_key = f"request_count:{client_identifier}"
    redis_client.incrby(request_key, 1)

def is_rate_limited(client_identifier):
    """
    Check if the client has exceeded the rate limit.
    """
    current_request_count = get_request_count(client_identifier)
    
    if current_request_count > REQUEST_LIMIT:
        # If the request count exceeds the limit, rate limit the request
        return True
    else:
        increment_request_count(client_identifier)
        return False

@app.route('/api', methods=['GET'])
def api():
    """
    Example endpoint where rate limiting will be applied.
    """
    client_identifier = get_client_identifier()

    if is_rate_limited(client_identifier):
        return jsonify({"error": "Rate limit exceeded. Try again later."}), 429

    return jsonify({"message": "Request successful!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
