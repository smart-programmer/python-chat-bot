from CHATBOT import db, login_manager
from datetime import datetime

class WebhookMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messagebird_request_string = db.Column(db.String(2000), nullable=False)
    message_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# example message.created event request
# {
#   "type": "message.created",
#   "contact": {
#     "id": "9354647c5b144a2b4c99f2n42497249",
#     "href": "https://rest.messagebird.com/1/contacts/9354647c5b144a2b4c99f2n42497249",
#     "msisdn": 316123456789,
#     "firstName": "Jen",
#     "lastName": "Smith",
#     "customDetails": {
#       "custom1": null,
#       "custom2": null,
#       "custom3": null,
#       "custom4": null
#     },
#     "createdDatetime": "2018-06-03T20:06:03Z",
#     "updatedDatetime": null
#   },
#   "conversation": {
#     "id": "2f719ebc5b144a18b75f44n12188288",
#     "contactId": "9354647c5b144a2b4c99f2n42497249",
#     "status": "active",
#     "createdDatetime": "2018-03-28T13:28:00Z",
#     "updatedDatetime": "2018-03-28T13:28:00Z",
#     "lastReceivedDatetime": "2018-03-28T13:28:00Z",
#     "lastUsedChannelId": "95e223e381364b00b1b21e52bbc6285e"
#   },
#   "message": {
#     "id": "8909570c5b71a40bb957f1n63383684",
#     "conversationId": "2f719ebc5b144a18b75f44n12188288",
#     "channelId": "2f719ebc5b144a18b75f44n12188288",
#     "status": "delivered",
#     "type": "text",
#     "direction": "sent",
#     "content": {
#       "text": "hello"
#     },
#     "createdDatetime": "2018-08-13T15:30:19Z",
#     "updatedDatetime": "2018-08-13T15:30:20Z"
#   }
# }