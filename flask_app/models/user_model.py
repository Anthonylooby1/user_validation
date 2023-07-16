from flask_app.config.mysqlconnect import connectToMySQL
from flask_app import DATABASE
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
ALPHA = re.compile(r"^[a-zA-Z]+$")

class User:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """   

        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM users WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_by_email(cls,data):
        query = """
            SELECT * FROM users WHERE email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @staticmethod
    def is_valid(data):
        is_valid = True
        if len(data['first_name']) < 1:
            flash('First name required', 'reg')
            is_valid = False
        elif len(data['first_name']) < 2:
             flash('First name must be at least two characters', 'reg')
             is_valid = False
        elif not ALPHA.match(data['first_name']):
            flash('first name can only contain letter','reg')
            is_valid = False
        if len(data['last_name']) < 1:
            flash('Last name required', 'reg')
            is_valid = False
        elif len(data['last_name']) < 2:
             flash('Last name must be at least two characters', 'reg')
             is_valid = False
        elif not ALPHA.match(data['last_name']):
            flash('Last name can only contain letter','reg')
            is_valid = False
        if len(data['email']) < 1:
            flash('email required', 'reg')
            is_valid = False    
        elif not EMAIL_REGEX.match(data['email']):
            flash('invalid email', 'reg')
            is_valid = False  
        else:
            potential_user = User.get_by_email({'email':data['email']})  
            if potential_user:
                 flash('email already exists', 'reg')
                 is_valid = False
        if len(data['password']) < 1:
            is_valid = False
            flash('Password required' 'reg') 
        elif len(data['password']) < 8:
            is_valid = False
            flash('Password must be at least 8 characters' 'reg')
        elif data['password'] != data['cpass']:
             is_valid = False
             flash('Password must match' 'reg')                   
        return is_valid    