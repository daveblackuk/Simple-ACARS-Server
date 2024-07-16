from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///acars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)  # Enable CORS for all routes

class ACARSMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    logon = db.Column(db.String(50), nullable=False)
    sender = db.Column(db.String(50), nullable=False)
    receiver = db.Column(db.String(50), nullable=False)
    message_type = db.Column(db.String(20), nullable=False)
    packet = db.Column(db.Text, nullable=True)  # Make packet nullable
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)

# Initialize the database
with app.app_context():
    db.create_all()

# CORS Headers decorator
@app.after_request
def after_request(response):
    # for testing using VSR
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:1228')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response

@app.route('/acars/system/connect.html', methods=['GET', 'POST'])
def connect():
    if request.method == 'POST':
        data = request.form
    else:
        data = request.args

    logon = " " # data.get('logon')
    sender = data.get('from')
    receiver = data.get('to')
    message_type = data.get('type')
    packet = data.get('packet')

    # Logging the received data for debugging
    print("Received data:")
#    print(f"logon: {logon}")
    print(f"from: {sender}")
    print(f"to: {receiver}")
    print(f"type: {message_type}")
    print(f"packet: {packet}")

    if not all([logon, sender, receiver, message_type]):
        missing_fields = [field for field in ['logon', 'from', 'to', 'type'] if not data.get(field)]
        return jsonify({"error": "Missing fields", "missing": missing_fields}), 400

    # Normalize fields to uppercase
    sender = sender.upper()
    receiver = receiver.upper()
  
    if message_type in ["cpdlc", "telex", "progress","position","posreq","datareq"]:
        new_message = ACARSMessage(
            logon=logon,
            sender=sender,
            receiver=receiver,
            message_type=message_type,
            packet=packet
        )
        db.session.add(new_message)
        db.session.commit()
        return "ok", 200

    elif message_type == "ping":
         return f"ok", 200
    
    elif message_type == "inforeq":
         return f"not implemented", 200

    elif message_type == "poll":
        messages = ACARSMessage.query.filter_by(receiver=sender, read=False).all()
        
        formatted_messages = " ".join([
            f"{{{msg.sender} {msg.message_type} {{{msg.packet}}}}}"
            for msg in messages
        ])
        
        for msg in messages:
            msg.read = True
            db.session.add(msg)
        db.session.commit()
        print(f"ok {formatted_messages}")
        return f"ok {formatted_messages}", 200

    elif message_type == "peek":
        # Retrieve messages from the last 24 hours and filter by sender
        since_date = datetime.utcnow() - timedelta(hours=24)
        messages = ACARSMessage.query.filter(ACARSMessage.timestamp >= since_date, ACARSMessage.receiver == sender).all()

        formatted_messages = " ".join([
            f"{{{msg.id} {msg.sender} {msg.message_type} {{{msg.packet}}}}}"
            for msg in messages
        ])
        print(f"ok {formatted_messages}")
        return f"ok {formatted_messages}", 200

    else:
        return jsonify({"error": "Unsupported message type"}), 400

@app.route('/dump', methods=['GET'])
def dump():
    messages = ACARSMessage.query.all()
    table_html = """
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Sender</th>
            <th>Receiver</th>
            <th>Message Type</th>
            <th>Packet</th>
            <th>Timestamp</th>
            <th>Read</th>
        </tr>
        {% for msg in messages %}
        <tr>
            <td>{{ msg.id }}</td>
            <td>{{ msg.sender }}</td>
            <td>{{ msg.receiver }}</td>
            <td>{{ msg.message_type }}</td>
            <td>{{ msg.packet }}</td>
            <td>{{ msg.timestamp }}</td>
            <td>{{ msg.read }}</td>
        </tr>
        {% endfor %}
    </table>
    """
    return render_template_string(table_html, messages=messages)

if __name__ == '__main__':
    print("0.3 fix peek")
    app.run(host='0.0.0.0', port=5050, debug=True)
