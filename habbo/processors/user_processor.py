from g_python.hmessage import HMessage
from g_python.hparsers import HEntity
from g_python.htools import RoomUsers

from habbo.managers import user_manager

def enter_user_processor(users):
   for profile in users: 
       user_manager.add_user(profile.index, profile.name, profile.id, profile.motto)
       
def leave_user_processor(message : HMessage):
    (user_room_id,) = message.packet.read("s")
    user_manager.remove_user(int(user_room_id))
        