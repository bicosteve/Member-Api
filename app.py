from flask import Flask,g

from connection import get_db, connect_db

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite3_db.close()

@app.route('/member', methods=['GET'])
def get_members():
    return 'all members'


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    return 'Returns one member by id'


@app.route('/member',methods=['POST'])
def add_member():
    return 'This adds a new member'

@app.route('/member/<int:member_id>', methods=['PUT','PATCH'])
def edit_member(member_id):
    return 'This updates member by id'

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    return 'deletes member from list by id'



if __name__ == '__main__':
    app.run(debug=True)
