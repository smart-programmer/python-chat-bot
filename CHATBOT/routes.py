from flask import Flask, request, redirect, render_template, url_for, make_response
from flask_mail import Message as MailMessage
from CHATBOT import app, db, bcrypt, mail, MAIL_USERNAME
from CHATBOT.models import WebhookMessage
from flask_login import current_user, login_user, login_required, logout_user





@app.route('/webhook', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        webhook_json_string = str(request.json) #https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
        webhookOBJ = WebhookMessage()
        webhookOBJ.messagebird_request_string = webhook_json_string
        db.session.add(webhookOBJ)
        db.session.commit()

    return str([i.messagebird_request_string for i in WebhookMessage.query.all()])

