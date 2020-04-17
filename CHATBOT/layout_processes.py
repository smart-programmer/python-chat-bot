import db
from messagebird import conversation_message 

# layout processes are reuseable functions and are the building blocks of layouts


def show_text_process(client, text, conversation_session):
    conversationObj_id = conversation_session.conversationObj_id
    channelObj_id = conversation_session.contact.channel.channelObj_id

    message = client.conversation_create_message(conversationObj_id, {
  'channelId': channelObj_id,
  'type': conversation_message.MESSAGE_TYPE_TEXT, 
  'content': {
    'text': text 
  }
})

    # return a boolean if the mssage got sent or not and any time the message fails the layout should either redo the step that or delete everything