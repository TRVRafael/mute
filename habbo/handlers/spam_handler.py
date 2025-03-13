from habbo.moderation import mute_player
from habbo.managers import room_manager, user_manager

def spam_handler(user_room_index, message): 
    user = user_manager.get_user_info(user_room_index)
    user_name = user['user_name']
    user_id = user['user_id']
    mute_player(user_id, room_manager.get_current_room_id(), user_name, message)