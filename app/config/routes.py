from system.core.router import routes

routes['default_controller'] = 'Quotes'
routes['POST']['/process/register'] = 'Quotes#register'
routes['POST']['/process/login'] = 'Quotes#process_login'
routes['/process/logout'] = 'Quotes#process_logout'
routes['/quotes'] = 'Quotes#quotes'
routes['POST']['/process/add_quote'] = 'Quotes#process_add_quote'
routes['POST']['/process/add_favorite'] = 'Quotes#process_add_favorite'
routes['POST']['/process/remove_favorite'] = 'Quotes#process_remove_favorite'
routes['/users/<user_id>'] = 'Quotes#users'