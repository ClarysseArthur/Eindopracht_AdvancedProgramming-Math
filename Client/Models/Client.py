class Client:
    def __init__(self, name, email):
        self.__name = name
        self.__email = email
        self.__ip = '0.0.0.0'
        self.__id = '12345'

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    @property
    def ip(self):
        return self.__ip

    @property
    def id(self):
        return self.__id

    def __str__(self):
        return f'Client: {self.name} - {self.email}'

    def __repr__(self):
        return f'Client: {self.name} - {self.email}'
