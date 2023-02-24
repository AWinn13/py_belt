from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DB, app
from flask_app.models import loginandreg
from flask_app.models import shows



class Like:
    def __init__(self , data ):
        self.user_id = data['user_id'],
        self.user_id = data['show_id']
        self.liker = None


    @classmethod
    def count_all(cls, data):
        query = " SELECT COUNT(likes.user_id) AS count from shows join likes on shows.id=likes.show_id where shows.id = %(show_id)s;"
        return connectToMySQL(DB).query_db(query, data)
    @classmethod
    def get_all(cls):
        query = " SELECT * from likes;"
        return connectToMySQL(DB).query_db(query)

    @classmethod
    def delete_like(cls, data):
        query  = "DELETE FROM likes WHERE user_id = %(user_id)s and show_id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    
    @classmethod
    def add_like(cls, data):
        query  = "Insert into likes (user_id, show_id) values (%(user_id)s , %(id)s);"
        return connectToMySQL(DB).query_db(query, data)
    
    

    # @classmethod
    # def get_all( cls ):
    #     query = "SELECT * FROM likes left join shows on likes.user_id = shows.user_id;"
    #     results = connectToMySQL(DB).query_db(query)
    #     if results:
    #         all_likes = []
    #         for row in results:
    #             this_like = cls(row)
                
    #             user_data= {
    #                 **row,
    #                 "id" : row["id"],
    #                 'created_at' : row['created_at'],
    #                 'updated_at' : row['updated_at']
    #             }
    #             show_data = {
    #                 'id' : row['id'],
    #                 'title' : row['title'],
    #                 'network' : row['network'],
    #                 'date' : row['date'],
    #                 'description' : row['description'],
    #                 'created_at' : row['created_at'],
    #                 'updated_at' : row['updated_at'],
    #                 'user_id' : row['user_id']
    #             }
    #             all_likes = []
    #             this_user = loginandreg.User(user_data)
    #             this_show = shows.Show(show_data)
    #             this_like.show = this_show
    #             this_like.liker = this_user
    #             all_likes.append(this_like)
    #         return all_likes
    #     return results
