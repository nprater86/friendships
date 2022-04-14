# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.friends = []
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('friendships_schema').query_db(query)
        # Create an empty list to append our instances of table
        users = []
        # Iterate over the db results and create instances of table with cls.
        for user_row in results:
            users.append( cls(user_row) )
        return users

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,NOW(),NOW());'
        return connectToMySQL('friendships_schema').query_db(query, data)

    @classmethod
    def get_all_users_with_friends(cls):
        query = 'SELECT * FROM users JOIN friends ON friends.user_id = users.id LEFT JOIN users AS users2 ON users2.id = friends.friend_id ORDER BY users.id, users2.first_name;'
        results = connectToMySQL('friendships_schema').query_db(query)
        users = []
        tempId = ''
        for row in results:
            if row["id"] != tempId:
                new_user = cls( row )
                users.append(new_user)
                tempId = new_user.id

            friend_data = {
                "id": row['users2.id'],
                "first_name": row['users2.first_name'],
                "last_name": row['users2.last_name'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }

            new_friend = User(friend_data)

            users[-1].friends.append(new_friend)

        return users

    @classmethod
    def find_friends_of_user(cls, id):
        query = 'SELECT * FROM users JOIN friends ON friends.user_id = users.id LEFT JOIN users AS users2 ON users2.id = friends.friend_id WHERE users.id = %(id)s;'
        results = connectToMySQL('friendships_schema').query_db(query, id)
        user = cls ( results[0] )
        for row in results:
            friend_data = {
                "id": row['users2.id'],
                "first_name": row['users2.first_name'],
                "last_name": row['users2.last_name'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }

            new_friend = User(friend_data)

            user.friends.append(new_friend)
        return user


    @classmethod
    def create_friendship(cls, data):
        query = 'INSERT INTO friends (user_id, friend_id, created_at, updated_at) VALUES (%(user_id)s, %(friend_id)s, NOW(), NOW());'
        return connectToMySQL('friendships_schema').query_db(query, data)