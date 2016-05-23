from system.core.model import Model
import re, time
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z ]+$') # Case insensitive "a" to "z" and "space" allowed
PASSWORD_REGEX = re.compile(r'^([^0-9]*|[^A-Z]*)$') # number and upper case letter allowed

class Quote(Model):
    def __init__(self):
        super(Quote, self).__init__()

    def register_user(self, info):
        errors = []
        if len(info['name']) < 2 or not NAME_REGEX.match(info['name']):
            errors.append("Invalid Name. (Letters only, at least 2 characters.)")
        if len(info['alias']) < 2 or self.db.query_db("SELECT * FROM users WHERE alias = '"+info['alias']+"'") != [] :
            errors.append("Invalid Alias. (At least 2 characters or Alias already in use.)")
        if len(info['email']) < 1 or not EMAIL_REGEX.match(info['email']):
            errors.append("Invalid Email Address.")
        if self.db.query_db("SELECT * FROM users WHERE email = '"+info['email']+"'") != [] :
            errors.append("Account already exists with this email. Please choose different email to register.")
        if len(info['password']) < 8:
            errors.append("Password must be more than 8 characters.")
            print "1111111zzzzvzcxvzcxv"
        elif info['password'] != info['confirm_password']:
            errors.append("Passwords do not match! Try again!")
            print errors
            print "1111111zzzz"
        # if PASSWORD_REGEX.match(info['confirm_password']):
        #     errors.append("Password requires to have at least 1 uppercase letter and 1 numeric value.")
        if info['date_of_birth'] == "" or info['date_of_birth'] > time.strftime("%Y-%m-%d"):
            print (time.strftime("%d/%m/%Y"))
            errors.append("Invalid Date of Birth.")
            print "finished!!"
        if errors != []:
            print "next step"
            return {
            'status': False,
            'errors': errors,
            }
        else:
            pw_hash = self.bcrypt.generate_password_hash(info['password'])
            title = info['name'].title() # capitalize first character of name (ex. john doe -> John Doe)
            user_query = "INSERT INTO users (name, alias, email, pw_hash, date_of_birth, created_at, updated_at) VALUES (:name, :alias, :email, :pw_hash, :date_of_birth, NOW(), NOW())"
            user_data = {
                'name': title,
                'alias': info['alias'],
                'email': info['email'],
                'pw_hash': pw_hash,
                'date_of_birth': info['date_of_birth']
                }
            user = self.db.query_db(user_query, user_data)
            new_user_id_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
            new_user_id_data = {'email': info['email']}
            new_user_id = self.db.query_db(new_user_id_query, new_user_id_data)
            return {
            'status': True,
            'user': new_user_id[0],
            }

    def login_user(self, info):
        user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        user_data = {'email': info['email']}
        user = self.db.query_db(user_query, user_data)
        if len(info['password']) < 8 or not EMAIL_REGEX.match(info['email']) or user == [] or not self.bcrypt.check_password_hash(user[0]['pw_hash'], info['password']):
            # message = "Wrong email and/or password." # login fails with all these if conditions
            return False
        else:
            return  (user[0]['id'], user[0]['name'])

    def add_quote(self, info, user_id):
        if len(info['author']) < 1 or len(info['message']) < 1:
            return False
        user_query = "INSERT INTO quotes (author, message, user_id, created_at, updated_at) VALUES (:author, :message, :user_id, NOW(), NOW())"
        user_data = {
            'author': info['author'],
            'message': info['message'],
            'user_id': user_id
            }
        user = self.db.query_db(user_query, user_data)
        return True

    def get_data(self):
        data = self.db.query_db("SELECT *, users.id as user_id, quotes.id as quote_id, favorites.id as favorite_id, favorites.user_id as fav_user_id FROM users LEFT JOIN quotes ON quotes.user_id = users.id LEFT JOIN favorites ON favorites.quote_id = quotes.id;")
        return data

    def add_favorite(self, info, user_id):
        user_query = "INSERT INTO favorites (user_id, quote_id, created_at, updated_at) VALUES (:user_id, :quote_id, NOW(), NOW())"
        user_data = {
            'user_id': user_id,
            'quote_id': info['quote_id']
            }
        user = self.db.query_db(user_query, user_data)
        return True

    def remove_favorite(self, info):
        self.db.query_db("DELETE FROM favorites WHERE id = " + info['favorite_id'])
        return True

    def get_user_data(self, user_id):
        data = self.db.query_db("SELECT users.id as user_id, users.name as name, quotes.author as author, quotes.message as message FROM users LEFT JOIN quotes ON quotes.user_id = users.id LEFT JOIN favorites ON favorites.quote_id = quotes.id WHERE users.id = " + user_id)
        count = self.db.query_db("SELECT COUNT(*) as count, users.id as user_id, users.name as name, quotes.author as author, quotes.message as message FROM users LEFT JOIN quotes ON quotes.user_id = users.id LEFT JOIN favorites ON favorites.quote_id = quotes.id WHERE users.id = " + user_id)
        return (data, count)