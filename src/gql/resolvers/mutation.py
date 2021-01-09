from ...database.crud import new_author


async def resolve_new_author(*_, username = None, email = None, password = None, passwordConfirm = None):

    
    if not username and email and password and passwordConfirm:
        raise Exception
    else:
        password_conf = passwordConfirm
        data = {
            'username': username,
            'email': email,
            'password': password,
            'conf_password': password_conf
        }
    
    result = await new_author(data)
    if result:
        return {'status': True, 'authorId': result}
    return {'status': False, 'error': 'Oops! Something happened'}

