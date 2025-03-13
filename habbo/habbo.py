import logging

from g_python.gextension import Extension
from g_python.hdirection import Direction
from g_python.htools import RoomUsers
from g_python.hpacket import HPacket


from habbo.callbacks import message_listener, leave_user_listener, enter_room_listener
from habbo.config.config import habbo_logger, ext
from habbo.processors import enter_user_processor


extension_info = {
    "title": "Torvi. Teste",
    "description": "Teste DIC",
    "version": "1.0",
    "author": "Torvi."
}


def run_extension():
    ext.start()
    habbo_logger.info("Habbo's G-Earth Extension running.")
    
    ext.intercept(Direction.TO_CLIENT, enter_room_listener, "GetGuestRoomResult")
    ext.intercept(Direction.TO_CLIENT, message_listener, "Chat")
    ext.intercept(Direction.TO_CLIENT, leave_user_listener, "UserRemove")
    room_users = RoomUsers(ext)
    room_users.on_new_users(enter_user_processor)
    ext.send_to_server(HPacket("GetHeightMap"))

