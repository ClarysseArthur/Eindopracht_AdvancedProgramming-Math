class Client:
    def __init__(self, name, email):
        self.__name = name
        self.__email = email

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    def __str__(self):
        return f'Client: {self.name} - {self.email}'

    def __repr__(self):
        return f'Client: {self.name} - {self.email}'
