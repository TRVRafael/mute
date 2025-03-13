from g_python.hmessage import HMessage

from habbo.processors import enter_user_processor, leave_user_processor, message_processor, enter_room_processor

def message_listener(message : HMessage):
    message_processor(message)
    
def enter_user_listener(message : HMessage):
   enter_user_processor(message)

def leave_user_listener(message : HMessage):
    leave_user_processor(message)

def enter_room_listener(message : HMessage):
    enter_room_processor(message)