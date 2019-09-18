from sym_api_client_python.listeners.room_listener import RoomListener
import logging


# sample implementation of Abstract RoomListener class
# has instance of SymBotClient so that it can respond to events coming in by leveraging other clients on SymBotClient
# each function should contain logic for each corresponding event
from python.message_processor import MessageProcessor


def log_event(comment, message):
    logging.debug(comment, message)


class RoomListenerImp(RoomListener):

    def __init__(self, sym_bot_client):
        self.bot_client = sym_bot_client
        self.msg_processor = MessageProcessor(self.bot_client)

    def on_room_msg(self, message):
        log_event('message received', message)
        self.msg_processor.process(message)

    def on_room_created(self, roomCreated):
        log_event('room was created', roomCreated)

    def on_room_deactivated(self, roomDeactivated):
        log_event('room Deactivated', roomDeactivated)

    def on_room_member_demoted_from_owner(self, roomMemberDemotedFromOwner):
        log_event('room member demoted from owner', roomMemberDemotedFromOwner)

    def on_room_member_promoted_to_owner(self, roomMemberPromotedToOwner):
        log_event('room member promoted to owner', roomMemberPromotedToOwner)

    def on_room_reactivated(self, roomReactivated):
        log_event('room reactivated', roomReactivated)

    def on_room_updated(self, roomUpdated):
        log_event('room updated', roomUpdated)

    def on_user_joined_room(self, userJoinedRoom):
        log_event('USER JOINED ROOM', userJoinedRoom)

    def on_user_left_room(self, userLeftRoom):
        log_event('USER LEFT ROOM', userLeftRoom)
