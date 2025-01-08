class Session:
    def __init__(self):
        self.username = None
        self.is_logged_in = False

    def login(self, username):
        self.username = username
        self.is_logged_in = True

    def logout(self):
        self.username = None
        self.is_logged_in = False

    def get_username(self):
        return self.username

    def is_logged_in(self):
        return self.is_logged_in
