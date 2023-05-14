from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from groceries_bot import GroceryAssistant

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

grocery_assistant = GroceryAssistant()

# Default route load index.html from ./template
@app.route('/')
def index():
    return render_template('index.html')


# Process user input
@app.route('/process_message', methods=['POST'])
def process_message():
    user_message = request.form.get('message')

    if 'shopping_list' not in session:
        session['shopping_list'] = []
    if 'temp_data' not in session:
        session['temp_data'] = []
    if 'current_state' not in session:
        session['current_state'] = "IDLE"
    
    response = grocery_assistant.process_message(user_message, session['shopping_list'], session['temp_data'], session['current_state'], session)
    
    session.modified = True

    return jsonify(response)


# Should set the lat and long of the user through browser
@app.route('/set_location', methods=['POST'])
def set_location():
    user_location = request.get_json()
    if user_location:
        session['user_location'] = user_location
        return "User location set", 200
    else:
        return "Failed to set user location", 400

if __name__ == '__main__':
    app.run(debug=True)