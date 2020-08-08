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
        self.room = [room]
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
        self.room[0] = room
        self.room.add_client(self)

    def remove_room(self):
        self.room.remove_client(self)
        self.room.clear()

    def get_room(self):
        return self.room[0]
    
    def add_friend(self, friend):
        self.friends.append(friend)
    
    def remove_friends(self, friend):
        self.friends.remove(self.friends.index(friend))
    

    

class Room():
    def __init__(self, name):
        self.name = name
        self.clients = []
    
    def add_clients(self, clients):
        self.clients = clients

    def add_client(self, client):
        self.clients.append(client)
    
    def remove_client(self, client):
        self.clients.remove(client)
    
    def get_clients(self):
        return self.clients
    
    def get_name(self):
        return self.name




class Home():
    def __init__(self):
        self.rooms = [Room("All")]
    
    def add_room(self, room):
        self.rooms.append(room)
    
    def remove_room(self, room): # Удалить комнату
        # Получаем комнату, которую надо удалить
        r = self.rooms[self.rooms.index(room)]
        # Говорим клиентам, которые подключены к этой комнате,
        # что они к ней больше не подключены
        for c in r.get_clients():
            c.remove_room()
        # Удаляем комнату
        self.rooms.remove(room)
    
    def remove_room_by_index(self, index):
        r = self.rooms[index]
        for c in r.get_clients():
            c.remove_room()
        self.rooms.remove(index)
    
    def remove_room_by_name(self, name):
        for r in self.rooms:
            if r.get_name() == name:
                for c in r.get_clients():
                    c.remove_room()
                self.rooms.remove(r)
                return
    
    def get_room(self, index):
        return self.rooms[index]

    def get_rooms(self):
        return self.rooms