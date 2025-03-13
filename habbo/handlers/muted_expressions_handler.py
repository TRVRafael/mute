from habbo.managers import user_manager, room_manager
from habbo.utils import is_dic
from habbo.config import habbo_logger
from habbo.moderation import ban_player
from data import db_controller
from habbo.utils import get_timestamp


def found_muted_expression_handler(found_muted_expression, message_text, user_room_id):
    user = user_manager.get_user_info(user_room_id)
    user_name = user['user_name']
    user_id = user['user_id']
    user_motto = user['user_motto']
    
    if is_dic(user_motto):
        print("dic")
        habbo_logger.info(f"Member {user_name} used muted expression {(found_muted_expression)} - {message_text}")
        return
    
    ban_player(user_id, room_manager.get_current_room_id(), user_name)
    
    for expression in found_muted_expression:
        db_controller.insert_affected(expression, user_name, message_text, get_timestamp())