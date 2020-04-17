import messagebird
from messagebird.conversation_message import MESSAGE_TYPE_HSM, MESSAGE_TYPE_TEXT

accessKey = "4LyuUQ5rrh2CT1Zwrql1hYuBW" # api key

client = messagebird.Client('4LyuUQ5rrh2CT1Zwrql1hYuBW', features=[messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANDBOX])
# print(client.request_plain_text("https://whatsapp-sandbox.messagebird.com/v1/conversations/8191d282593f49809be22df4394e4c0a/messages?limit=20"))
# print(client.request_plain_text("https://whatsapp-sandbox.messagebird.com/v1/conversations/8191d282593f49809be22df4394e4c0a")) this returns type str
# print(type(client.request("https://rest.messagebird.com/lookup/966503681868"))) # .request returns type DICT
# .request_store_as_file() this stores in a file

# messages = client.conversation_list_messages("8191d282593f49809be22df4394e4c0a", limit=20)
# print(messages)
# print(client.message_list().items)

webhook_request_dict = {
    "events": ["message.created", "message.updated"], # i guess message.updated is when a message turns from pending to read and like that
    "channelId": "7e4da85010004d32a1427e4a2edcee33",
    "url": "https://chatbo-webhook-endpoint.herokuapp.com/webhook"
  }
# client.conversation_create_webhook(webhook_request_dict)
print(client.conversation_list_webhooks())
# client.conversation_delete_webhook('139062c3875c4ac1a9706f4b9b3753ce')

# first step start a conversation using an HSM
# conversation = client.conversation_start({
#   'channelId': '7e4da85010004d32a1427e4a2edcee33',
#   'to': '966503681868',
#   'type': MESSAGE_TYPE_HSM,
#   'content': {
#     'hsm': {
#       'namespace': '78b0f3fa_30cc_4cd3_b681_a9d1c794a7a4',
#       'templateName': 'support',
#       'language': {
#         'policy': 'deterministic',
#         'code': 'en'
#       },
#       'params': [
#         {"default": "Roberto"},
#         {"default": "123"},
#         {"default": "new coffee machine"},
#         {"default": "MessageBird, Trompenburgstraat 2C, 1079TX Amsterdam"},
#       ]
#     }
#   }
# })

# print(client.conversation_list_messages("8191d282593f49809be22df4394e4c0a", limit=20))


# # response was 
# """{
#   "id": "8191d282593f49809be22df4394e4c0a",
#   "contactId": "1443164a34a24db3bb928ff094cb5111",
#   "contact": {
#     "id": "1443164a34a24db3bb928ff094cb5111",
#     "href": "",
#     "msisdn": 966503681868,
#     "displayName": "966503681868",
#     "firstName": "",
#     "lastName": "",
#     "customDetails": {},
#     "attributes": {},
#     "createdDatetime": "2020-04-11T15:10:15Z",
#     "updatedDatetime": "2020-04-11T15:10:15Z"
#   },
#   "channels": [
#     {
#       "id": "7e4da85010004d32a1427e4a2edcee33",
#       "name": "Sandbox",
#       "platformId": "whatsapp",
#       "status": "active",
#       "createdDatetime": "2019-06-05T11:44:25Z",
#       "updatedDatetime": "2019-12-11T16:47:16Z"
#     }
#   ],
#   "status": "active",
#   "createdDatetime": "2020-04-11T15:10:14Z",
#   "updatedDatetime": "2020-04-11T20:03:36.047669646Z",
#   "lastReceivedDatetime": "2020-04-11T20:03:36.0416706Z",
#   "lastUsedChannelId": "7e4da85010004d32a1427e4a2edcee33",
#   "messages": {
#     "totalCount": 8,
#     "href": "https://whatsapp-sandbox.messagebird.com/v1/conversations/8191d282593f49809be22df4394e4c0a/messages",
#     "lastMessageId": "d6ae87b7cdce4707a8eb8b62cf2c1710"
#   }
# }"""


# after a conversation is initiated we can send the client normal messages for 24 hours and they can reply: NOTE: this is at least what happend in the sanbox maybe it's different in production

# second step have a conversation with the client in the 24 hour window

msg = client.conversation_create_message('8191d282593f49809be22df4394e4c0a', {
  'channelId': '7e4da85010004d32a1427e4a2edcee33',
  'type': MESSAGE_TYPE_TEXT, 
  'content': {
    'text': "هلاااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااا"
  }
})




#response

# """{
#   "id": "19fa205a240e4de59da25f456094ea38",
#   "conversationId": "8191d282593f49809be22df4394e4c0a",
#   "platform": "whatsapp",
#   "channelId": "7e4da85010004d32a1427e4a2edcee33",
#   "type": "text",
#   "content": {
#     "text": "ok"
#   },
#   "direction": "sent",
#   "status": "pending",
#   "createdDatetime": "2020-04-11T20:16:51.1082409Z",
#   "updatedDatetime": null
# }"""


# balanceOBJ = client.balance()

# print("my balance is: {}".format(balanceOBJ.amount))