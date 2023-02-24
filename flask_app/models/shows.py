from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DB, app
from flask_app.models import loginandreg
from flask_app.models import likes



class Show:
    def __init__(self , data ):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.date = data['date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.spotter = None
        self.liker = None
        self.unliker = None


    #-------------------Create-------------------------------------
    @classmethod
    def create_show(cls, data):
        query = "INSERT INTO shows (title, network, date, description, user_id) VALUES (%(title)s, %(network)s, %(date)s, %(description)s, %(user_id)s);" 
        return connectToMySQL(DB).query_db(query, data)
    
    
    
    # -----------------------Update show-----------------------------------------
    @classmethod
    def update_show(cls, data):
        query = "UPDATE shows SET title=%(title)s,network=%(network)s,description=%(description)s,date=%(date)s, user_id=%(user_id)s WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db( query, data )
    
    # --------------Delete------------------------------
    @classmethod
    def delete_show(cls, data):
        query  = "DELETE FROM shows WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    

    
    # -----------------------Get all ONE TO MANY--------------------------
    
    @classmethod
    def get_all( cls ):
        query = "SELECT * FROM shows left join users on shows.user_id = users.id;"
        results = connectToMySQL(DB).query_db(query)
        
        if results:
            
            all_shows = []
            
            for row in results:
                this_show = cls(row)
                
                user_data= {
                    **row,
                    "id" : row["users.id"],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                }
                like_data = {
                    'show_id' : row['id'],
                    'user_id' : row['users.id']
                }
                this_user = loginandreg.User(user_data)
                this_show.liker = likes.Like(like_data)
                
                this_show.spotter = this_user
                all_shows.append(this_show)
            
            return all_shows
        return results
    
    # -----------------------Get One ONE TO MANY-------------------------
    @classmethod
    def get_one_show(cls, data):
        query = "SELECT * FROM shows left JOIN users ON users.id = shows.user_id WHERE shows.id= %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        if results:
            this_show = cls(results[0])
            row = results[0]
            user_data= {
                    **row,
                    "id" : row["users.id"],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at'],
                }
            like_data = {
                    'show_id' : row['id'],
                    'user_id' : row['users.id']
                }

            num_of_likes= likes.Like.count_all(like_data)
            this_show.likes = num_of_likes[0]['count']
            this_user = loginandreg.User(user_data)
            this_show.spotter = this_user
            return this_show
        return this_show
    
    
    



    # ---------------------Validation-----------
    @staticmethod
    def validate_show(data):
        is_valid = True
        if len(data['title']) < 3:
            flash("title must be at least 3 characters.")
            is_valid = False
        if len(data['network']) < 3:
            flash("network must be at least 3 characters.")
            is_valid = False
        if len(data['description']) < 3:
            flash("descriptions must be at least 3 characters.")
            is_valid = False
        if len(data['date']) < 1:
            flash("Date cannot be blank.")
            is_valid = False
        return is_valid
