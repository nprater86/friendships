from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User

@app.route('/')
def index():
    users = User.get_all()
    users_with_friends = User.get_all_users_with_friends()

    return render_template('index.html', users = users, users_with_friends = users_with_friends)

@app.route('/add_user', methods=["POST"])
def add_user():
    data={
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
    }
    User.save(data)
    return redirect('/')

@app.route('/create_friendship', methods=["POST"])
def create_friendship():
    #check if user_id = friends_id
    if request.form['friend_id'] == request.form['user_id']:
        print('Cannot be friends with yourself!')
        return redirect('/')

    #if not, create user
    id = {"id":request.form["user_id"]
    }
    user = User.find_friends_of_user(id)

    #check if friend is already in friends
    for friend in user.friends:
        if str(request.form['friend_id']) == str(friend.id):
            print('Friendship already exists!')
            return redirect('/')

    #if above two checks clear, then execute below
    data = {
        "user_id":request.form["user_id"],
        "friend_id":request.form["friend_id"]
    }
    User.create_friendship(data)
    
    return redirect('/')