import random

class ROOM:
    def __init__(self, room_name, first_user, rooms):
        """
        room chat for server
        :param room_name: string type, the new room name
        :param first_user: USER type, the first user in room
        :param rooms: dictionary of string and ROOM, rooms (ROOM) according to rooms names (string)
        """
        self.room_name = ''
        if room_name not in rooms:
            self.room_name = room_name
        self.users = [first_user]

    def join_room(self, user):
        """
        joining user to the room
        :param user: USER type, the user who joining to the room
        :return: none
        """
        self.users.append(user)

    def pass_message(self, sender, message):
        """
        pass message from user to all the rest of users
        :param sender: USER type, who send the message
        :param message: string type, the message
        :return: none
        """
        for user in self.users:
            if user != sender:
                user.send_message(sender.user_name + ': ' + message)
