from CHATBOT import db
from CHATBOT.layout_processes import show_text_process, send_image_process
from CHATBOT.models import MenueModel, ViewableObjectModel, ViewableObjectAttribute, LayoutModel
from CHATBOT.utils import get_attribute, increment_step_counter, get_text
from CHATBOT.objects import LngObj
# define layouts logic


def new_contact_layout(client, conversation_session): # new_contact_layout should be a somple message then a registration process
    # to do
    contact = conversation_session.contact
    bot = contact.bot
    message = conversation_session.message
    lngobj = LngObj.translate("new_contact_layout", bot.language)
    if conversation_session.step_counter == 0:
        # to do: simple welcoming message
        show_text_process(client, get_text("greeting", lngobj), conversation_session) # after we create customer models this should be a string of text with the prefered language of the customer that's extracted from a language file like the old bot
        conversation_session.step_counter += 1
        db.session.commit() 
        return False
    elif conversation_session.step_counter == 1:
        show_text_process(client, get_text("name-confirmation", lngobj).format(message), conversation_session)
        contact.name = message
        conversation_session.step_counter += 1
        db.session.commit()
        return False
    elif conversation_session.step_counter == 2: 
        if (message == "yes"):
            return True
        else:
            show_text_process(client, "تم حذف الاسم رجاء اعد التسجيل", conversation_session)
            db.session.delete(conversation_session)
            db.session.delete(contact)
            db.session.commit()
        return False
    return False

def show_menue_layout(client, conversation_session): # a menue could be implemented by the ViewableObject model insted of a MenueModel
    menues = MenueModel.query.filter_by(bot=conversation_session.contact.bot)
    menue_string = "menue\n\n"
    for menue in menues:
        menue_string += menue.command + ": " + menue.description + "\n"
    show_text_process(client, menue_string, conversation_session)

def show_products_prices_layout(client, conversation_session): # steps: 1- create layout Model 2- create menue with the layout 3- create viewable objects if needed step 4- write logic
    bot = conversation_session.contact.bot
    layout = LayoutModel.query.filter_by(name=conversation_session.layout_name).first()
    menue = MenueModel.query.get(conversation_session.menue_id)
    lngobj = LngObj.translate("show_scheduled_times_layout", bot.language)
    viewable_objects = ViewableObjectModel.query.filter_by(layout=layout, bot=bot, menue=menue).all()
    if conversation_session.step_counter == 0:
        string = "our products\n\n"
        for index, vb in enumerate(viewable_objects): # add a description attribute so we can add description to things like pre build pc's
            attributes = vb.attributes 
            string += "\n{} : {}\npress {} to see product details \n".format(get_attribute(attributes, "product_name"), get_attribute(attributes, "product_price"), index)
        string += "\ntype exit to return to menue"
        show_text_process(client, string, conversation_session)
        increment_step_counter(conversation_session)
        return False
    elif conversation_session.step_counter == 1:
        message = conversation_session.message
        index = None
        if message == "exit":
            return True
        else:
            try:
                index = int(message)
            except:
                show_text_process(client, "incorrect command", conversation_session)
                return False
            try:
                viewable_object = viewable_objects[index]
            except:
                show_text_process(client, "no prodct with this index", conversation_session)
                return False

            description = get_attribute(viewable_object.attributes, "product_description")
            image = get_attribute(viewable_object.attributes, "product_image")

            if image != "":
                send_image_process(client, image, description, conversation_session)
            elif description == "":
                show_text_process(client, "no description for this product", conversation_session)
            else:
                show_text_process(client, description, conversation_session)
        

def static_layout(client, conversation_session):
    pass

def command_not_exists_layout(client, conversation_session):
    show_text_process(client, "no such command exists", conversation_session)


def schedule_appointments_layout(client, conversation_session):
    pass

def show_scheduled_times_layout(client, conversation_session): # 
    # this layout can be used to show work times and such
    bot = conversation_session.contact.bot
    layout = LayoutModel.query.filter_by(name=conversation_session.layout_name).first()
    menue = MenueModel.query.get(conversation_session.menue_id)
    lngobj = LngObj.translate("show_scheduled_times_layout", bot.language)
    week = ViewableObjectModel.query.filter_by(layout=layout, bot=bot, menue=menue).first()
    if week:
        attributes = week.attributes
        sunday = get_attribute(attributes, "sunday")
        monday = get_attribute(attributes, "monday")
        tuesday = get_attribute(attributes, "tuesday")
        wednesday = get_attribute(attributes, "wednesday")
        thursday = get_attribute(attributes, "thursday")
        friday = get_attribute(attributes, "friday")
        saturday = get_attribute(attributes, "saturday")
        
        schedule_string = get_text("schedule_string", lngobj).format(sunday, monday, tuesday, wednesday, thursday, friday, saturday)
        show_text_process(client, schedule_string, conversation_session)
    else:
        show_text_process(client, "no chedule available", conversation_session)
    return True


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
