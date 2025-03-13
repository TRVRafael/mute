from g_python.hmessage import HMessage

from habbo.managers import Message, spam_detector
from habbo.handlers import found_muted_expression_handler, spam_handler
from data import db_controller


def message_processor(message: HMessage):
    (user_room_index, message_text, *_) = message.packet.read("isiiii")
    # if check_command(message_text):
    #     handle_command(message_text)
    
    # found_expressions = search_for_word(message_text)
    # if found_expressions:
    #     mute_player(1)
    msg = Message(user_room_index, message_text)
    if msg.is_valid_command():
        msg.handle_command()
    
    founded_muted_expressions = msg.contains_muted_expressions(db_controller.get_muted_expressions())
    if founded_muted_expressions:
        found_muted_expression_handler(founded_muted_expressions, msg._message_text, user_room_index)
    
    if msg.check_spam():
        spam_handler(user_room_index, msg._message_text)
        
        
    
        
        