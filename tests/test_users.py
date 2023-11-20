import data.users as usrs

def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0  # at least one user!
    
    for key, user in users.items():
        assert isinstance(key.USERNAME, str)
        assert len(user[usrs.USERNAME], str)
        assert user[usrs.USERNAME] not in [u[usrs.USERNAME] for u in users.values()]

        password = user[usrs.PASSWORD]
        assert isinstance(password, str)
        assert len(password) >= usrs.MIN_PASSWORD_LEN
        assert any(char.isdigit() for char in password) #at least one digit in password
        assert any(char.isalpha() for char in password) #at least one letter in password
        assert any(char in "!@$&*/" for char in password) # At least one special character in password