from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update_data():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({
        'status': 'success',
        'message': f'Data updated at {current_time}'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
