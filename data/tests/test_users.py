import data.users as usrs

def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0  # at least one user!
    for key in users:
        assert isinstance(key.USERNAME, str)
        assert len(key.USERNAME) >= usrs.MIN_USER_NAME_LEN
        assert len(key.PASSWORD) >= usrs.MIN_PASSWORD_LEN
        user = users[key]
        # assert isinstance(user, dict)