from .. import endpoints
import json
import os
FIRST_NAME_KEY = 'first_name'
LAST_NAME_KEY = 'last_name'
USERNAME_KEY = 'username'
EMAIL_KEY = 'email'
PASSWORD_KEY = 'password'
RES_HALL_KEY = 'res_hall'
ADDRESS_KEY = 'address'
PRONOUNS_KEY = 'pronouns'
FOLLOWERS_KEY = 'followers'
FOLLOWING_KEY = 'following'
MARKET_DESC_KEY = 'market_desc'

FIRST_NAME = 'First Name'
LAST_NAME = 'Last Name'
USERNAME = 'my_username'
EMAIL = 'myemail@email.com'
PASSWORD = 'mypassword'
RES_HALL = 'Apple Hall'
ADDRESS = '60 New St'
PRONOUNS = 'they/them'
FOLLOWERS = []
FOLLOWING = []
MARKET_DESC = ""

os.environ['CLOUD_MONGO'] = '1'
app = endpoints.app.test_client()

def test_health_check():
    print(f'/{endpoints.HEALTH_CHECK}')
    response = app.get(f'/{endpoints.HEALTH_CHECK}')
    assert response.status_code == 201
    

def test_users_post():
    data = {
		FIRST_NAME_KEY: FIRST_NAME,
		LAST_NAME_KEY: LAST_NAME,
		USERNAME_KEY: USERNAME,
		EMAIL_KEY: EMAIL,
		PASSWORD_KEY: PASSWORD,
		RES_HALL_KEY: RES_HALL,
		ADDRESS_KEY: ADDRESS,
		PRONOUNS_KEY: PRONOUNS
	}

    response = app.post(f'/{endpoints.USERS}', json=data)
    assert response.status_code == 201
    
def test_user_get():
    response = app.get(f'/{endpoints.USERS}/my_username')
    assert response.status_code == 200
    
def test_user_delete():
    delete_response = app.delete(f'/{endpoints.USERS}/delete/my_username')
    assert delete_response.status_code == 200
    

