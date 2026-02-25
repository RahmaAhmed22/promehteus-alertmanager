from flask import Flask, jsonify, abort
from prometheus_client import start_http_server, Counter, Gauge, Summary, Histogram
import random
import time

app = Flask(__name__)
c = Counter('my_requests_total', 'Counts number of different requests', ['path'])
g = Gauge('my_inprogress_requests', 'Requests in progress', ['path'])
s = Summary('request_latency_seconds', 'Request latency in seconds', ['path'])
h = Histogram('request_latency_seconds_h', 'Request latency in seconds', ['path'], buckets=[0.3, 0.5, 1, 2, 3, 4, 5, 6])

# 1. Success Endpoint (HTTP 200)
@app.route('/success')
def get_success():
    c.labels(path='success').inc()

    g.labels(path='success').inc()
    t = random.random() * 10
    start_time = time.time()
    time.sleep(t)
    g.labels(path='success').dec()
    
    s.labels(path='success').observe(time.time() - start_time)
    h.labels(path='success').observe(time.time() - start_time)
    
    return jsonify({
        "status": "success",
        "message": "Everything is working perfectly!"
    }), 200

# 2. Bad Request Endpoint (HTTP 400)
@app.route('/bad-request')
def get_bad_request():
    c.labels(path='bad-request').inc()
    
    g.labels(path='bad-request').inc()
    t = random.random() * 10
    start_time = time.time()
    time.sleep(t)
    g.labels(path='bad-request').dec()
    
    s.labels(path='bad-request').observe(time.time() - start_time)
    h.labels(path='bad-request').observe(time.time() - start_time)
    
    # Used when the server cannot process the request due to client error
    abort(400, description="Payload is missing required fields.")

# 3. Forbidden/Failure Access Endpoint (HTTP 403)
@app.route('/forbidden')
def get_forbidden():
    c.labels(path='forbidden').inc()
    
    g.labels(path='forbidden').inc()
    t = random.random() * 10
    start_time = time.time()
    time.sleep(t)
    g.labels(path='forbidden').dec()
    
    s.labels(path='forbidden').observe(time.time() - start_time)
    h.labels(path='forbidden').observe(time.time() - start_time)
    
    # Used when the server understands the request but refuses to authorize it
    abort(403, description="You do not have permission to view this resource.")

@app.route('/fail-server')
def trigger_server_error():
    c.labels(path='fail-server').inc()
    
    g.labels(path='fail-server').inc()
    t = random.random() * 10
    start_time = time.time()
    time.sleep(t)
    g.labels(path='fail-server').dec()
    
    s.labels(path='fail-server').observe(time.time() - start_time)
    h.labels(path='fail-server').observe(time.time() - start_time)
    
    # This manually triggers a "Server Error" response
    abort(500, description="The server encountered a critical internal error.")

# Error handlers to return JSON instead of default HTML pages
@app.errorhandler(400)
def handle_bad_request(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(403)
def handle_forbidden(e):
    return jsonify(error=str(e)), 403

@app.errorhandler(500)
def handle_500(e):
    return jsonify(error="Internal Server Error", message="Something went wrong on our end."), 500

if __name__ == '__main__':
# Start the Prometheus metrics server on port 8001
    start_http_server(8001)
    app.run(host='0.0.0.0', port=5000)