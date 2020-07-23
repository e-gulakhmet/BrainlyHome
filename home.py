class Client():
    """

    Класс клиента.

    У каждого клиента(девайса) имеется:
    номер(не изменяется),
    тип(relay, button, ...)(изменяется девайсом),
    имя(изменяется пользователем),
    статус подключения(изменяется),
    комната, которой он принадлежит(изменяется пользователем),
    Друзья - клиенты, сообщения которых мы слушаем

    """

    def __init__(self, id, kind, name="Unknown", status=False, room=None):
        self.id = id
        self.kind = kind
        self.name = name
        self.status = status
        self.room = room
        self.friends = []
    
    def get_id(self): # Получить номер клиента
        return self.id

    def set_kind(self, kind): # Изменить тип у клиента
        self.kind = kind

    def get_kind(self): # Получить тип клиента
        return self.kind

    def set_name(self, name): # Изменить имя у клиента
        self.name = name
        
    def get_name(self): # Получить имя клиента
        return self.name
    
    def set_status(self, status):
        self.status = status
    
    def get_status(self):
        return self.status

    def set_room(self, room):
        self.room = room

    def get_room(self):
        return self.room

    def add_friends(self, friends):
        self.friends.extend(friends)
    
    def add_friend(self, friend):
        self.friends.append(friend)
    

    

class Room():
    def __init__(self, name):
        self.name = name
        self.clients = []
    
    def add_clients(self, clients):
        self.clients.extend(clients)

    def add_client(self, client):
        self.clients.append(client)
    
    def get_clients(self):
        return self.clients
    
    def get_name(self):
        return self.name