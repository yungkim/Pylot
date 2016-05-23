from system.core.controller import *

class Quotes(Controller):
    def __init__(self, action):
        super(Quotes, self).__init__(action)
        self.load_model('Quote')
        self.db = self._app.db
   
    def index(self):
        return self.load_view('index.html')

    def quotes(self): # main page after login/registration
        data = self.models['Quote'].get_data()
        print data
        return self.load_view('quotes.html', data=data)

    def register(self):
        user_info = self.models['Quote'].register_user(request.form)
        if user_info['status'] == True:
            session['id'] = user_info['user']['id'] 
            session['name'] = user_info['user']['name']            
            return redirect ('/quotes')
        else:
            for message in user_info['errors']:
                # print "error!!#!@"
                flash(message)
                return redirect('/')

    def process_login(self):
        user = self.models['Quote'].login_user(request.form)
        if user:
            session['id'],session['name']  = user
            return redirect('/quotes')
        flash( "Wrong email and/or password.")
        return redirect('/')

    def process_logout(self):
        session.clear()
        return redirect('/')

    def process_add_quote(self):
        print session['id']
        quote = self.models['Quote'].add_quote(request.form, session['id'])
        if quote == False:
            flash("Content cannot be empty.")
        return redirect('/quotes')

    def process_add_favorite(self):
        favorite = self.models['Quote'].add_favorite(request.form, session['id'])
        if favorite == False:
            flash("Content cannot be empty.")
        return redirect('/quotes')

    def process_remove_favorite(self):
        # data = self.models['Quote'].get_data()
        # print data
        favorite = self.models['Quote'].remove_favorite(request.form)
        if favorite == False:
            flash("Content cannot be empty.")
        return redirect('/quotes')

    def users(self, user_id): 
        data = self.models['Quote'].get_user_data(user_id)[0]
        count = self.models['Quote'].get_user_data(user_id)[1]
        return self.load_view('users.html', data=data, count=count, user_id=user_id)