"""
This module interfaces to our user data.
"""
USERNAME = "username"
PASSWORD = "password"
MIN_USER_NAME_LEN = 6
MIN_PASSWORD_LEN = 8

def get_users():
    users = {
        
		"user_one": {
            USERNAME: "test_username_1", 
            PASSWORD: "12345"   
		},
        
        "user_two": {
            USERNAME: "test_username_2", 
            PASSWORD: "12345"      
		},
        "user_three": {
            USERNAME: "test_username_3", 
            PASSWORD: "12345"   
		},
        
	}
    
	
    return users
