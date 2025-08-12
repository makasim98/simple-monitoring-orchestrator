from flask import Flask, request, jsonify

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


@app.route('/add')
def add_endpoint():
    return "<h1>ADDING</h1>" # return HTML

@app.route('/remove')
def remove_endpoint():
    return "<h1>REMOVING</h1>" # return HTML

app.run(host="0.0.0.0", port=5000, debug=True)