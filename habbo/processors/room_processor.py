from g_python.hmessage import HMessage

from habbo.managers import room_manager

def enter_room_processor(message : HMessage):
    _ = message.packet.read_bool()
    room_id = message.packet.read_int()
    
    room_manager.set_current_room_id(room_id)