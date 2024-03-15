from lib.event_manager import EventManager

USERS = {
    "admin": {
        "name": "Admin",
        "avatar": "https://api.dicebear.com/7.x/adventurer/svg?seed=SysAdmin",
        "password": "admin",
    },
    "user": {
        "name": "User",
        "avatar": "https://api.dicebear.com/7.x/adventurer/svg?seed=RandomUser",
        "password": "user",
    },
}


async def user_event_handler(data):
    print("User Event Fired! Data: " + str(data))
    action = data.get("action")

    if action == "login":
        print("Logging in user!")
        username = data.get("username")
        password = data.get("password")
        found = USERS.get(username)

        if found and found.get("password") == password:
            print("User logged in!")
            return {
                "message": "User logged in!",
                "user": {"name": found.get("name"), "avatar": found.get("avatar")},
            }
        else:
            raise Exception("Invalid username or password!")

    elif action == "logout":
        print("Logging out user!")
        return {"message": "User logged out!"}


def register_user_events(event_manager: EventManager):
    event_manager.register("user-event", user_event_handler)
