from CHATBOT import db

def set_object_field(name, parsed_json):

    if parsed_json != None:
        return parsed_json[name] if name in parsed_json else None
    return None

def reset_conversation_session(conversation_session): # maybe also delete conversationObj_id if it changes over time
    conversation_session.layout_name = None
    conversation_session.step_number = 0
    if len(conversation_session.arguments) > 0:
        for arg in conversation_session.arguments:
            db.session.delete(arg)
    conversation_session.arguments.clear()
    db.session.commit()


def update_session_message(message, conversation_session):
    conversation_session.message = message
    db.session.commit()