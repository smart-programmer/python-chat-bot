from CHATBOT import db


from messagebird.conversation_message import MESSAGE_TYPE_HSM, MESSAGE_TYPE_TEXT

# layout processes are reuseable functions and are the building blocks of layouts


def show_text_process(client, text, conversation_session):
  conversationObj_id = conversation_session.conversationObj_id
  channelObj_id = conversation_session.contact.bot.channel.channelObj_id

  # return a boolean if the mssage got sent or not and any time the message fails the layout should either redo the step that or delete everything
  msg = client.conversation_create_message(conversationObj_id, {
        'channelId': channelObj_id,
        'type': MESSAGE_TYPE_TEXT, 
        'content': {
            'text': text # text can't be an empty string like this "" or it will fail
        }
    })

  