from flask import Flask, jsonify, request

app=Flask(__name__)

@app.route('/')
def root():
    return 'Hola Manuel'

@app.route('/users/<user_id>')
def get_user(user_id):
    user = {
        "id": user_id,
        "name": "Manuel",
        "tel": "7772601600"
    }
    return jsonify(user), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    data["status"] = 'Usuario creado' 
    return jsonify(data), 201


if __name__=='__main__':
    app.run(debug=True)