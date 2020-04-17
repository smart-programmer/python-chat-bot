from flask import Flask, request, redirect, render_template, url_for, make_response
from flask_mail import Message as MailMessage
from CHATBOT import app, db, bcrypt, mail, MAIL_USERNAME
from CHATBOT.models import WebhookMessage
from flask_login import current_user, login_user, login_required, logout_user
from webhook_handlers import message_created_handler, message_updated_handler
from messagebird import conversation_webhook
from messagebird import Client



# When the first message is sent or received from a user, a conversation is automatically created for them.

message_bird_api_access_key = "4LyuUQ5rrh2CT1Zwrql1hYuBW"


@app.route('/webhooks', methods=['GET', 'POST']) # note this needs to handle PUT(update)
def webhook():
    if request.method == "POST":
        webhook_json_string = str(request.json) # https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
        webhookOBJ = WebhookMessage()
        webhookOBJ.messagebird_request_string = webhook_json_string
        db.session.add(webhookOBJ)
        db.session.commit()

    return "<h1>{}</h1>".format(str([i.messagebird_request_string for i in WebhookMessage.query.all()]))


@app.route('/webhook') 
def webhook_endpoint():
    client = Client(message_bird_api_access_key, features=[messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANDBOX])

    # handle incoming message
     
    if request.method == "POST":
        webhook_json_string = str(request.json)
        if webhook_json_string["type"] == conversation_webhook.CONVERSATION_WEBHOOK_EVENT_MESSAGE_CREATED:
            message_created_handler(client, webhook_json_string)

        webhookOBJ = WebhookMessage()
        webhookOBJ.messagebird_request_string = webhook_json_string
        db.session.add(webhookOBJ)
        db.session.commit()


        elif webhook_json_string["type"] == conversation_webhook.CONVERSATION_WEBHOOK_EVENT_MESSAGE_UPDATED:
            message_updated_handler(client, webhook_json_string)

    return "<h1>{}</h1>".format(str([i.messagebird_request_string for i in WebhookMessage.query.all()]))
