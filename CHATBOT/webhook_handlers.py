from messagebird import Client
from CHATBOT import db
from CHATBOT.objects import ConversationObj, MessageObj, MessageContentObj, ContactObj, HSMObj
from CHATBOT.models import ConversationSessionModel, ContactModel, ChannelModel, MenueModel, LayoutModel, ConversationSessionArgModel, BotModel
import json
from CHATBOT.layout_logic import new_contact_layout, static_layout, command_not_exists_layout, show_menue_layout, show_products_prices_layout, show_scheduled_times_layout
from CHATBOT.layout_processes import show_text_process, send_image_process
from CHATBOT.utils import reset_conversation_session, update_session_message
# webhook logic handelrs


def message_created_handler(client, webhook_json_string):
    # handle incoming json string
    # don't forget to write the logic that determans if it's a message from a contact or from us 
    # don't forget to make this platform specefic because if don't customers will own the same bot for all platforms
    
    messageObj = MessageObj(json.loads(webhook_json_string)["message"])
    if messageObj.direction == "sent":
        return
    message = messageObj.content["text"]
    if not message:
        return
    contactObj = ContactObj(json.loads(webhook_json_string)["contact"])
    conversationObj = ConversationObj(json.loads(webhook_json_string)["conversation"]) # COMPLETE
    channelObj_id = messageObj.channelId
    channel = ChannelModel.query.filter_by(channelObj_id=channelObj_id).first()
    bot = channel.bot
    if bot == None:
        return 

    # handle message result
    # if we know contact then do this if he got a session then complete and so on
    # if customer first incounter create a conversation session and if not pull conversation session
    contact = ContactModel.query.filter(ContactModel.number==str(contactObj.number), ContactModel.bot_id==bot.id).first() # RESEARCH multiple filters
    if contact:
        # determan layout name
        conversation_session = contact.session
        update_session_message(message, conversation_session)
        layout_name = None
        if conversation_session.layout_name != None:
            layout_name = conversation_session.layout_name
        else:
            menue = MenueModel.query.filter(MenueModel.command==message, MenueModel.bot_id==bot.id).first()
            if (not menue):
                command_not_exists_layout(client, conversation_session) 
                show_menue_layout(client, conversation_session)
                return
            layout_name = menue.layout.name # simple: look for the layout of the menue that the user picked for example if he picked from the menue command number 4 we search for which layout command number 4 should follow
            conversation_session.layout_name = layout_name
            conversation_session.menue_id = menue.id
            db.session.commit()

        # handle conversation depending on the message layout
        if layout_name == "new_contact":
            finished = new_contact_layout(client, conversation_session)
            if finished:
                reset_conversation_session(conversation_session)
                show_menue_layout(client, conversation_session) # COMPLETE # call show menue at the finish of every layout
            return
        elif layout_name == "show_products": # a product is a viewable object with two attributes a product_name and a product_price
            finished = show_products_prices_layout(client, conversation_session)
            if finished:
                reset_conversation_session(conversation_session)
                show_menue_layout(client, conversation_session)
            return
        elif layout_name == "show_scheduled_times":
            finished = show_scheduled_times_layout(client, conversation_session)
            if finished:
                reset_conversation_session(conversation_session)
                show_menue_layout(client, conversation_session)
            return

        elif layout_name == "reserve_appointment_layout":
            # this is like an event layout the customer provides data (in this case what times are free) then we show that data to the user and then the user registers for a given hour with his information then we send a message to a given number that a user has registred or a given date (this only has 1 problem which is that the customer has to prvide which information the user should provide for each appointment) 
            pass
    
        elif layout_name == None:
            show_menue_layout(client, conversation_session)
            reset_conversation_session(conversation_session)
            return
        else:
            show_text_process(client, "not layout", conversation_session)
    else:
        # handle new contact create a session and a contact and add him to the right channel
        contact = ContactModel(number=str(contactObj.number), bot=bot)
        conversation_session = ConversationSessionModel(layout_name="new_contact", step_counter=0, contact=contact, conversationObj_id=conversationObj.id, message=message)
        db.session.add(contact)
        db.session.add(conversation_session)
        db.session.commit()
        new_contact_layout(client, conversation_session)
        return



def message_updated_handler(webhook_json_string):
    pass


