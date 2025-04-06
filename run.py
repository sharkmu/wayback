import flask
from waybackpy import WaybackMachineAvailabilityAPI
import time

app = flask.Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    start_time = time.time()
    result = None
    if flask.request.method == "POST":
        url = flask.request.form.get("url")
        user_agent = "Wayback Tool"
        try:
            availability_api = WaybackMachineAvailabilityAPI(url, user_agent)
            oldest = availability_api.oldest()
            timestamp = availability_api.timestamp()
            
            result = {
                "input_url": url,
                "oldest_snapshot": oldest,
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"Error: {e}")
            result = False
    
    end_time = time.time()
    action_time = round(end_time - start_time, 2)
    return flask.render_template("index.html", result=result, action_time=action_time)

if __name__ == "__main__":
    app.run(debug=True)