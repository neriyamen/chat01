import random

class ROOM:
    # room chat for server

    def __init__(self, first_user, rooms):
        self.room_id = self.create_room_id(rooms)
        self.users = [first_user]

    def create_room_id(self, rooms):
        # create new id for the room
        room_id = random.randint(100000, 999999)
        while room_id in rooms:
            room_id = random.randint(100000, 999999)
        return room_id

    def join_room(self, user):
        # joining user to the room
        self.users.append(user)

    def pass_message(self, sender, message):
            # pass message from user to all the rest of users
        for user in self.users:
            if user != sender:
                user.send_message(sender.user_name + ': ' + message)
