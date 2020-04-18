from flask import Flask, request, redirect, render_template, url_for, make_response
from flask_mail import Message as MailMessage
from CHATBOT import app, db, bcrypt, mail, MAIL_USERNAME
from CHATBOT.models import WebhookMessage
from flask_login import current_user, login_user, login_required, logout_user
from CHATBOT.webhook_handlers import message_created_handler, message_updated_handler
from messagebird import conversation_webhook
from messagebird import Client
import messagebird
import json
from messagebird.conversation_message import MESSAGE_TYPE_HSM, MESSAGE_TYPE_TEXT




# When the first message is sent or received from a user, a conversation is automatically created for them.

message_bird_api_access_key = "4LyuUQ5rrh2CT1Zwrql1hYuBW"


@app.route('/webhook', methods=['GET', 'POST']) # note this needs to handle PUT(update)
def webhook():
    if request.method == "POST":
        webhook_json_string = str(request.json) # https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
        webhookOBJ = WebhookMessage()
        webhookOBJ.messagebird_request_string = webhook_json_string
        db.session.add(webhookOBJ)
        db.session.commit()
        client = messagebird.Client('4LyuUQ5rrh2CT1Zwrql1hYuBW', features=[messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANDBOX])
        if not request.json["type"] == "sent":
            msg = client.conversation_create_message('8191d282593f49809be22df4394e4c0a', {
    'channelId': '7e4da85010004d32a1427e4a2edcee33',
    'type': MESSAGE_TYPE_TEXT, 
    'content': {
        'text': "هلاااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااا"
    }
})

    return "<h1>{}</h1>".format(str([i.messagebird_request_string for i in WebhookMessage.query.all()]))


@app.route('/webhooks', methods=['GET', 'POST']) 
def webhook_endpoint():
    client = Client(message_bird_api_access_key, features=[messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANDBOX])

    # handle incoming message
   
     
    if request.method == "POST":
        webhook_json_string = json.dumps(request.json)
        webhookOBJ = WebhookMessage()
        webhookOBJ.messagebird_request_string = webhook_json_string
        db.session.add(webhookOBJ)
        db.session.commit()
        webhook_parsed_string = json.loads(webhook_json_string)
        if webhook_parsed_string["type"] == conversation_webhook.CONVERSATION_WEBHOOK_EVENT_MESSAGE_CREATED:
            message_created_handler(client, webhook_json_string)


        # elif webhook_parsed_string["type"] == conversation_webhook.CONVERSATION_WEBHOOK_EVENT_MESSAGE_UPDATED:
        #     return "<h1>{}</h1>".format(str([i.messagebird_request_string for i in WebhookMessage.query.all()]))
            # message_updated_handler(client, webhook_json_string)



      

    return "<h1>{}</h1>".format(str([i.messagebird_request_string for i in WebhookMessage.query.all()]))
