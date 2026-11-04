users = []
next_id = 1


def create_user(user_data):
    global next_id

    user = user_data.model_dump()
    user["id"] = next_id

    users.append(user)
    next_id += 1

    return user


def get_all_users():
    return users


def get_user_by_id(user_id):
    for user in users:
        if user["id"] == user_id:
            return user

    return None
def update_user(user_id, user_data):
    for user in users:
        if user["id"] == user_id:
            user.update(user_data.model_dump())
            return user

    return None


def delete_user(user_id):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return True

    return False