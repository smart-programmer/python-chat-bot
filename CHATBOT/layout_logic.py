from CHATBOT import db
from CHATBOT.layout_processes import show_text_process
from CHATBOT.models import MenueModel
# define layouts logic


def new_contact_layout(client, conversation_session): # new_contact_layout should be a somple message then a registration process
    # to do
    contact = conversation_session.contact
    message = conversation_session.message
    if conversation_session.step_counter == 0:
        # to do: simple welcoming message
        show_text_process(client, "السلام عليكم ورحمة الله وبركاته اهلا وسهلا بك في بوت المساند, الرجاء ادخال الاسم للبدء", conversation_session) # after we create customer models this should be a string of text with the prefered language of the customer that's extracted from a language file like the old bot
        conversation_session.step_counter += 1
        db.session.commit() 
        return False
    elif conversation_session.step_counter == 1:
        show_text_process(client, "نعم, لا", conversation_session)
        contact.name = message
        conversation_session.step_counter += 1
        db.session.commit()
        return False
    elif conversation_session.step_counter == 2: 
        if (message == "نعم"):
            return True
        else:
            show_text_process(client, "السلام عليكم ورحمة الله وبركاته اهلا وسهلا بك في بوت المساند, الرجاء ادخال الاسم للبدء", conversation_session)
            db.session.delete(conversation_session)
            db.session.delete(contact)
            db.session.commit()
        return False
    return False

def show_menue_layout(client, conversation_session): # a menue could be implemented by the ViewableObject model insted of a MenueModel
    menues = MenueModel.query.filter_by(channel_id=conversation_session.contact.channel.id)
    menue_string = "hey\n"
    for menue in menues:
        menue_string += menue.command + " - " + menue.description + "\n"
    show_text_process(client, menue_string, conversation_session)

def show_products_prices_layout(conversation_session):

    pass

def static_layout(conversation_session):
    # to do
    pass

def command_not_exists_layout(client, conversation_session):
    # to do
    show_text_process(client, "no such command exists", conversation_session)


def event_layout(conversation_session):

    # if conversation_session.step_counter == 0:
    #     for event in events:
    #         if event.has_image:
    #             show_image_process(event.image, event.description)
    #         else:
    #             show_text_process(event.description)
        
    # elif conversation_session.step_counter == 1:
    #     finished = registration_process(client, conversation_session, # we pass what the user should register and the start message and the end message)
    #     # how should we design the registration process and what arguments  how do we tell it what we want the user to provide and where do we store what the user provided
    #     if finished:
    #         return True
    #     else:
    #         conversation_session.step_counter += 1
    #         db.session.commit()
            
    pass
