from flask import Flask,g, request,jsonify
from functools import wraps

from connection import get_db, connect_db

app = Flask(__name__)

api_username = 'osama'
api_password = 'osama123@'

#authentication function
def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args,**kwargs)
        return jsonify({'message':'Authentication failed'})

    return decorated

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite3_db.close()

@app.route('/member', methods=['GET'])
@protected
def get_members():

    db = get_db()
    members_cur = db.execute('select id, name, email, level from members')
    members = members_cur.fetchall()

    all_members = []

    for member in members:
        member_dict = {}
        member_dict['id'] = member['id']
        member_dict['name'] = member['name']
        member_dict['email'] = member['email']
        member_dict['level'] = member['level']

        all_members.append(member_dict)

    return jsonify ({'members':all_members})


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    db = get_db()
    member_cur = db.execute('select id, name, email, level from members where id = ?',[member_id])
    member = member_cur.fetchone()

    return jsonify({'member':{'id':member['id'],\
    'name':member['name'],'email':member['email'],'level':member['level']}})


@app.route('/member',methods=['POST'])
@protected
def add_member():
    member_data = request.get_json()

    name = member_data.get('name')
    email = member_data.get('email')
    level = member_data.get('level')

    db = get_db()
    db.execute('insert into members (name,email,level) values (?,?,?)',[name,email,level])
    db.commit()

    member_cur = db.execute('select id,name,email,level from members where name = ?',[name])
    new_member = member_cur.fetchone()

    return jsonify({'id':new_member['id'], 'name':new_member['name'],'email':new_member['email'],'level':new_member['level']})

@app.route('/member/<int:member_id>', methods=['PUT','PATCH'])
@protected
def edit_member(member_id):
    new_data = request.get_json()

    name = new_data['name']
    email = new_data['email']
    level = new_data['level']

    db = get_db()
    db.execute('update members set name = ?, email = ?, level = ? where id = ?', [name, email, level, member_id])
    db.commit()

    member_cur = db.execute('select id, name, email, level from members where id = ?',[member_id])
    new_member = member_cur.fetchone()

    return jsonify({'member':{'id':new_member['id'], 'name':new_member['name'], 'email':new_member['email'], 'level':new_member['level']}})

@app.route('/member/<int:member_id>', methods=['DELETE'])
@protected
def delete_member(member_id):
    db = get_db()
    cur = db.execute('delete from members where id = ?',[member_id])
    db.commit()

    return jsonify ({'message':'The member id has been deleted'})





if __name__ == '__main__':
    app.run(debug=True)
