from lib.event_manager import EventManager

def register_message_events(event_manager: EventManager):
    async def test_event_handler(data):
        print("Test Event Fired! Data: " + str(data))
        return {"message": "Test Event Handled!"}

    event_manager.register("message-test", test_event_handler)
