from CHATBOT import db

from messagebird.conversation_message import MESSAGE_TYPE_HSM, MESSAGE_TYPE_TEXT

# layout processes are reuseable functions and are the building blocks of layouts


def show_text_process(client, text, conversation_session):
  conversationObj_id = conversation_session.conversationObj_id
  channelObj_id = conversation_session.contact.channel.channelObj_id

  #     message = client.conversation_create_message("8191d282593f49809be22df4394e4c0a", {
  #   'channelId': '7e4da85010004d32a1427e4a2edcee33',
  #   'type': conversation_message.MESSAGE_TYPE_TEXT, 
  #   'content': {
  #     'text': text 
  #   }
  # })# return a boolean if the mssage got sent or not and any time the message fails the layout should either redo the step that or delete everything
  msg = client.conversation_create_message('8191d282593f49809be22df4394e4c0a', {
          'channelId': '7e4da85010004d32a1427e4a2edcee33',
          'type': MESSAGE_TYPE_TEXT, 
          'content': {
              'text': str(text)
          }

  