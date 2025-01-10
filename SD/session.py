class Session:
    def __init__(self):
        self.logged_in = False
        self.username = None  # Store only the username

    def login(self, username):
        self.logged_in = True
        self.username = username  # Store the username when logged in

    def logout(self):
        self.logged_in = False
        self.username = None

    def is_logged_in(self):
        return self.logged_in

    def get_username(self):
        return self.username  # Return the username
