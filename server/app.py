from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# GET /messages: returns an array of all messages as JSON, ordered by created_at in ascending order.
# POST /messages: creates a new message with a body and username from params, and returns the newly created post as JSON.
# PATCH /messages/<int:id>: updates the body of the message using params, and returns the updated message as JSON.
# DELETE /messages/<int:id>: deletes the message from the database.

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET','POST'])
def get_messages():

    query = Message.query.order_by(Message.created_at.asc()).all()
    if not query:
        return make_response({'message':'There are no messages'},404)
    if request.method == 'GET':
        messages_to_return = [message.to_dict() for message in  query]
        return make_response(messages_to_return,200)
    elif request.method == 'POST':
        # message = Message(
        #     body = body,
        #     username= username,
            
        # )
        data = request.json
        body = data.get('body')
        username = data.get('username')

        if not username or not body:
            return make_response({'error':'Both body and user must be provided'},400)
        message = Message(
             body = body,
             username= username,
        )

        db.session.add(message)
        db.session.commit()
        message_dict = message.to_dict()
        return make_response(message_dict,201)





# PATCH /messages/<int:id>: updates the body of the message using params, and returns the updated message as JSON.
# DELETE /messages/<int:id>: deletes the message from the database.
@app.route('/messages/<int:id>', methods=['PATCH','DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id = id).first()
    if not message:
        return make_response({'message':f'There is no message with an id of {id}'})
    
    if request.method == 'PATCH':
        data = request.json
        body = data.get('body')
        if not body:
            return make_response({'message':'The body must be provided for a Patch request'})
        message.body = body
        db.session.commit()
        message_dict = message.to_dict()
        return make_response(message_dict, 200)
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.commit()
        response = {
            'succsessfuly_deleted':True,
            'message':'The message has been deleted'

        }
        return make_response(response,200)

    

if __name__ == '__main__':
    app.run(port=5555)
