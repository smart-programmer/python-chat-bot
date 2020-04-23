from flask import Flask, request, redirect, render_template, url_for, make_response
from flask_mail import Message as MailMessage
from CHATBOT import app, db, bcrypt, mail, MAIL_USERNAME
from CHATBOT.models import WebhookMessage, BotModel, MenueModel, LayoutModel, ViewableObjectModel, ViewableObjectAttribute, User
from CHATBOT.forms import MenueForm, ProductsForm, BotForm, RegisterForm, LoginForm
from flask_login import current_user, login_user, login_required, logout_user
from CHATBOT.webhook_handlers import message_created_handler, message_updated_handler
from CHATBOT.utils import get_attribute
from messagebird import conversation_webhook
from messagebird import Client
import messagebird
import json
from messagebird.conversation_message import MESSAGE_TYPE_HSM, MESSAGE_TYPE_TEXT




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
        client = messagebird.Client('4LyuUQ5rrh2CT1Zwrql1hYuBW', features=[messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANDBOX])
        if request.json["type"] == "message.created":
            if not request.json["message"]["direction"] == "sent":
                msg = client.conversation_create_message('8191d282593f49809be22df4394e4c0a', {
        'channelId': '7e4da85010004d32a1427e4a2edcee33',
        'type': MESSAGE_TYPE_TEXT, 
        'content': {
            'text': "هلاااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااااا"
        }
    })

    return "<h1>{}</h1>".format(str([i.messagebird_request_string for i in WebhookMessage.query.all()]))


@app.route('/webhook', methods=['GET', 'POST']) 
def webhook_endpoint():
    client = messagebird.Client('4LyuUQ5rrh2CT1Zwrql1hYuBW', features=[messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANDBOX])

    # handle incoming message
   
     
    if request.method == "POST":
        webhook_json_string = json.dumps(request.json)
        webhookOBJ = WebhookMessage()
        webhookOBJ.messagebird_request_string = webhook_json_string
        db.session.add(webhookOBJ)
        db.session.commit()
        webhook_parsed_string = json.loads(webhook_json_string)
        if request.json["type"] == "message.created":
            message_created_handler(client, webhook_json_string)


        # elif webhook_parsed_string["type"] == conversation_webhook.CONVERSATION_WEBHOOK_EVENT_MESSAGE_UPDATED:
        #     return "<h1>{}</h1>".format(str([i.messagebird_request_string for i in WebhookMessage.query.all()]))
            # message_updated_handler(client, webhook_json_string)



      

    return "<h1>{}</h1>".format(str([i.messagebird_request_string for i in WebhookMessage.query.all()]))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=False)
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("index"))
            else:
                return redirect(url_for("login"))
        else:
            return redirect(url_for("login"))

    return render_template("login.html", form=form)

@app.route("/register")
def register(): 
    form = RegisterForm()

    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, full_name=form.full_name.data, number=form.number.data,
        email=form.email.data, password=password)
        db.session.add(user)
        db.session.commit()

    return render_template("register.html", form=form)

@app.route("/log_out")
@login_required
def log_out():
    logout_user()
    return redirect(url_for("index"))


@app.route("/bots")
@login_required
def bots(): # C
    return render_template("bots.html")

# create an update route for everything creatable like the bot don't make update and create in the same route
# and when someon requests to see a certan object just take him to the update page of that object

@app.route("/bot/<int:bot_id>", methods=["GET", "POST"])
@login_required
def bot(bot_id): # C
    form = BotForm()
    bot = BotModel.query.get(bot_id)

    if not bot or not bot.user == current_user:
        return redirect(url_for('index'))
    else:
        form.name = bot.name

    if form.validate_on_submit():
        bot.name = form.name
        db.session.add(bot)

        db.session.commit()

    return render_template("bot.html", bot=bot, form=form)

@app.route("/bot_create", methods=["GET", "POST"])
@login_required
def create_bot(bot_id): 
    form = BotForm()
   
    if form.validate_on_submit():
        bot = BotModel(name=form.name)
        db.session.append(bot)
        db.session.commit()

    return render_template("bot_create.html", form=form)


@app.route("/menue/<int:menue_id>", methods=["GET", "POST"])
@login_required
def menue(menue_id, bot_id):
    form = MenueForm()

    menue = MenueModel.query.get(menue_id)
    if not menue or not menue.bot in current_user.bots:
        return redirect(url_for('index'))
    
    form.layout.data = menue.layout.name
    form.command.data = menue.command
    form.description.data = menue.description
    
    if form.validate_on_submit():
        layout = LayoutModel.query.filter_by(name=form.layout)
        menue.description = form.description.data
        menue.layout = layout
        menue.command = form.command.data
        db.session.add(menue)
        db.session.commit()
        
    return render_template("menue.html", form=form, menue=menue)
    

@app.route("/menue_create/<int:bot_id>", methods=["GET", "POST"])
def menue_create(bot_id):
    form = MenueForm()
    bot = BotModel.query.get(bot_id)
    if form.validate_on_submit():
        menue = MenueModel(bot=bot, layout=LayoutModel.query.filter_by(name=form.layout.data), description=form.description.data, command=form.command.data)
        db.session.add(menue)
        db.session.commit()
    return render_template("menue_create.html", form=form)


@app.route("/viewable_objects_router/<layout_name>/<int:bot_id>")
def viewable_objects_router(layout_name):
    layouts = LayoutModel.query.all()
    for layout in layouts:
        if layout.name == layout_name:
            return 
    if layout_name == "show_products":
        return redirect(url_for("products", bot_id=bot_id))
    elif layout_name == "events":
        return redirect(url_for("events", bot_id=bot_id))
    elif layout_name == "schedule_appointment":
        return redirect(url_for("appointments", bot_id=bot_id))

    return redirect(url_for("index")) 

@app.route("/products/<int:bot_id>/<layout_name>")
def products(bot_id, layout_name):

    bot = BotModel,query.get(bot_id)
    if not bot or not bot.user == current_user:
        return redirect(url_for("index"))

    layout = LayoutModel.query.filter_by(name=layout_name)
    if not layout or layout not in bot.layouts:
        return redirect(url_for("index"))

    products = ViewableObjectModel.quey.filter_by(bot=bot, layout=layout).all()
    name_values = []
    for product in products:
        attributes = product.attributes
        name = get_attribute(attributes, "product_name")
        if name:
            name_values.append(name)

    return render_template("products.html", products=name_values)


@app.route("/product/<int:bot_id>")
@app.route("/product/<int:product_id>/<int:bot_id>")
def product(product_id, bot_id):
    form = ProductsForm()
    bot = BotModel.query.get(bot_id)
    if not bot or not bot.user == current_user:
        return redirect(url_for("index"))
    product = ViewableObjectModel.query.get(product_id)
    if product:
        if not product.bot == bot:
            return redirect(url_for("index"))
        else: 
            form.description.data = product.description
            form.name.data = product.name
            form.price.data = product.price

    if form.validate_on_submit():
        product = ViewableObjectModel(layout=layout, bot=bot)
        name = ViewableObjectAttribute(name="product_name", value=form.name.data viewable_object=product)
        price = ViewableObjectAttribute(name="product_price", value=str(form.price.data), viewable_object=product)
        description = ViewableObjectAttribute(name="product_description", value=form.description.data, viewable_object=product)
        db.session.add(product)
        db.session.add(name)
        db.session.add(price)
        db.session.add(description)
    db.session.commit()
    return render_template("product.html", form=form)

# add delete to everything that's creatable like bots and add update also