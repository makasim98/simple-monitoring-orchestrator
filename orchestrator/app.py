from flask import Flask, jsonify

app = Flask("Orchestrator")

monitored_endpoints = {}

@app.route('/')
def dashboard():
    return '''
    <h1>Orchestrator Dashboard!!!</h1>
        <p>Manage your monitored endpoints here.</p>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; width: 400px; margin: 40px auto;">
                <div style="background: #ffffff; border: 1px solid #000000; height: 100px; display: flex; align-items: center; justify-content: center;">Box 1</div>
                <div style="background: #ffffff; border: 1px solid #000000; height: 100px; display: flex; align-items: center; justify-content: center;">Box 2</div>
                <div style="background: #ffffff; border: 1px solid #000000; height: 100px; display: flex; align-items: center; justify-content: center;">Box 3</div>
                <div style="background: #ffffff; border: 1px solid #000000; height: 100px; display: flex; align-items: center; justify-content: center;">Box 4</div>
                <div style="background: #ffffff; border: 1px solid #000000; height: 100px; display: flex; align-items: center; justify-content: center;">Box 5</div>
                <div style="background: #ffffff; border: 1px solid #000000; height: 100px; display: flex; align-items: center; justify-content: center;">Box 6</div>
                <div style="background: #ffffff; border: 1px solid #000000; height: 100px; display: flex; align-items: center; justify-content: center;">Box 7</div>
                <div style="background: #ffffff; border: 1px solid #000000; height: 100px; display: flex; align-items: center; justify-content: center;">Box 8</div>
                <div style="background: #ffffff; border: 1px solid #000000; height: 100px; display: flex; align-items: center; justify-content: center;">Box 9</div>
            </div>
            '''


# Get endpoint monitored by the Orchestrator
@app.route('/enpoints')
def add_endpoint():
    return "<h1>ADDING</h1>" # return HTML

# ADD New Endpoint to the monitored APIs
@app.route('/add_enpoint')
def add_endpoint():
    return "<h1>ADDING</h1>" # return HTML

# Remove existing Endpoint from the monitored APIs
@app.route('/remove_enpoint')
def remove_endpoint():
    return "<h1>REMOVING</h1>" # return HTML

# Deploy monitoring client to target remote server/vm
@app.route('/deploy')
def deploy_client():
    return "<h1>REMOVING</h1>" # return HTML

# Remove monitoring client from target remote server/vm
@app.route('/un-deploy')
def remove_client():
    return "<h1>REMOVING</h1>" # return HTML

# Set resource tresholds
@app.route('/thresholds')
def remove_client():
    return "<h1>REMOVING</h1>" # return HTML


app.run(host="0.0.0.0", port=5000, debug=True)