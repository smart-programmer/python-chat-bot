from CHATBOT import db

def set_object_field(name, parsed_json):

    if parsed_json != None:
        return parsed_json[name] if name in parsed_json[name] else None
    return None

def reset_conversation_session(conversation_session): # maybe also delete conversationObj_id if it changes over time
    conversation_session.layout_name = None
    conversation_session.step_number = 0
    db.session.delete(conversation_session.arguments)
    conversation_session.arguments = None
    db.session.commit()