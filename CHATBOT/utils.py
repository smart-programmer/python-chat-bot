import os
import json
from CHATBOT import app
from CHATBOT import db
import datetime

def set_object_field(name, parsed_json):

    if parsed_json != None:
        return parsed_json[name] if name in parsed_json else None
    return None

def reset_conversation_session(conversation_session): # maybe also delete conversationObj_id if it changes over time
    conversation_session.layout_name = None
    conversation_session.step_counter = 0
    if len(conversation_session.arguments) > 0:
        for arg in conversation_session.arguments:
            db.session.delete(arg)
    conversation_session.arguments.clear()
    db.session.commit()


def update_session_message(message, conversation_session):
    conversation_session.message = message
    db.session.commit()

def get_attribute(attributes_list, attribute_name):
    attribute = None
    for attrib in attributes_list:
        if attrib.name == attribute_name:
            attribute = attrib.value
            break
            
    return attribute


def set_user_language(response, language):
	expire_date = datetime.datetime.now()
	expire_date = expire_date + datetime.timedelta(days=100000)
	response.set_cookie("language", language, expires=expire_date)


def read_language_file(page_name, language):
    path = os.path.join(app.root_path, "static", "languages", language + ".json")

    with open(path, "r", encoding='utf-8') as f:
        language_dict = json.loads(f.read())
        page_list = language_dict[page_name]
        return page_list


def increment_step_counter(conversation_session):
    conversation_session.step_counter += 1
    db.session.commit()