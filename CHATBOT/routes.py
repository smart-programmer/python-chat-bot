
from flask import Flask, request, redirect, render_template, url_for, make_response
from flask_mail import Message as MailMessage
from CHATBOT import app, db, bcrypt, mail, MAIL_USERNAME
from CHATBOT.models import WebhookMessage, BotModel, MenueModel, LayoutModel, ViewableObjectModel, ViewableObjectAttribute, User, ChannelModel
from CHATBOT.forms import MenueForm, ProductsForm, BotForm, RegisterForm, LoginForm, ChannelForm, LanguageForm, LayoutForm, Bot_channel_linkerForm, ScheduledTimesForm
from flask_login import current_user, login_user, login_required, logout_user
from CHATBOT.webhook_handlers import message_created_handler, message_updated_handler
from CHATBOT.objects import LngObj
from CHATBOT.utils import get_attribute, set_user_language
from messagebird import conversation_webhook
from messagebird import Client
import messagebird
import json
from messagebird.conversation_message import MESSAGE_TYPE_HSM, MESSAGE_TYPE_TEXT





# When the first message is sent or received from a user, a conversation is automatically created for them.

message_bird_api_access_key = "4LyuUQ5rrh2CT1Zwrql1hYuBW"
client = messagebird.Client(message_bird_api_access_key, features=[messagebird.Feature.ENABLE_CONVERSATIONS_API_WHATSAPP_SANDBOX])
webhook_route = "webhook"
# consider implementing a system for multiple api accesss keys so in the future there maybe more than one

@app.context_processor
def utility_processor():
    def get_text(tag, language_list):
        return next(x.get("description") for x in language_list if x.get("tag") == tag)
    return dict(get_text=get_text)


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
        if request.json["type"] == "message.created":
            message_created_handler(client, webhook_json_string)


        # elif webhook_parsed_string["type"] == conversation_webhook.CONVERSATION_WEBHOOK_EVENT_MESSAGE_UPDATED:
        #     return "<h1>{}</h1>".format(str([i.messagebird_request_string for i in WebhookMessage.query.all()]))
            # message_updated_handler(client, webhook_json_string)



      

    return "<h1>{}</h1>".format(str([i.messagebird_request_string for i in WebhookMessage.query.all()]))


@app.route("/")
def index():
    form = LanguageForm()
    cookie = request.cookies.get("language")
    if not cookie:
        default_language = "ar"
        lngObj = LngObj.translate('index', default_language)
        response = make_response(render_template("index.html", form=form, language_list=lngObj))
        set_user_language(response, default_language)
        return response
    else:
        form.language.default = cookie
        form.process()

    lngObj = LngObj.translate('index', cookie)
    response = make_response(render_template("index.html", form=form, language_list=lngObj))
    
    return response

@app.route("/set_language", methods=["POST"])
def set_language():
    language = request.form.get("language")
    response = make_response(redirect(url_for('index')))
    if language:
        set_user_language(response, language)
    return response


@app.route("/login", methods=["GET", "POST"])
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

@app.route("/register", methods=["GET", "POST"])
def register(): 
    form = RegisterForm()

    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, full_name=form.full_name.data, number=form.number.data,
        email=form.email.data, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("register.html", form=form)

@app.route("/log_out")
@login_required
def logout():
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
    form = LanguageForm()

    bot = BotModel.query.get(bot_id)
   

    if not bot or not bot.user == current_user:
        return redirect(url_for('index'))

    if form.validate_on_submit():
        bot.language = form.language.data
        db.session.commit()
        return redirect(url_for("bot", bot_id=bot_id))
    form.language.default = bot.language
    form.process()

    return render_template("test.html", bot=bot, form=form, lang=bot.language)

@app.route("/bot_create", methods=["GET", "POST"])
@login_required
def create_bot(): # C
    form = BotForm()
   
    if form.validate_on_submit():
        bot = BotModel(name=form.name.data, user=current_user, number=form.number.data)
        db.session.add(bot)
        db.session.commit()
        return redirect(url_for("bots"))

    return render_template("bot_create.html", form=form)

@app.route("/bot_delete/<int:bot_id>")
@login_required
def delete_bot(bot_id): 

    bot = BotModel.query.get(bot_id)

    if not bot or not bot.user == current_user:
        return redirect(url_for('index'))
   

    db.session.delete(bot)
    db.session.commit()
    return redirect(url_for("bots"))


@app.route("/update_bot/<int:bot_id>", methods=["GET", "POST"])
@login_required
def update_bot(bot_id):
    form = BotForm()
    bot = BotModel.query.get(bot_id)

    if not bot or not bot.user == current_user:
        return redirect(url_for('index'))

    if request.method == "GET":
        form.name.data = bot.name
    
    if form.validate_on_submit():
        bot.name = form.name.data
        db.session.add(bot)
        db.session.commit()

    return render_template("update_bot.html", form=form)


@app.route("/menue/<int:menue_id>", methods=["GET", "POST"])
@login_required
def menue(menue_id):
    form = MenueForm()
    

    menue = MenueModel.query.get(menue_id)
    if not menue or not menue.bot in current_user.bots:
        return redirect(url_for('index'))

    bot = menue.bot
    
    if request.method == "GET":
        form.layout.data = menue.layout.name
        form.command.data = menue.command
        form.description.data = menue.description

    layouts = bot.layouts
    layout_choices = []
    for layout in layouts:
        layout_choices.append([layout.name, layout.name])
    form.layout.choices = layout_choices
    
    if form.validate_on_submit():
        layout = LayoutModel.query.filter_by(name=form.layout.data).first()
        if not layout in menue.bot.layouts:
            return redirect(url_for("menue", menue_id=menue_id))
        menue.description = form.description.data
        menue.layout = layout
        menue.command = form.command.data
        db.session.add(menue)
        db.session.commit()
        return redirect(url_for("menue", menue_id=menue_id))
        
    return render_template("menue.html", form=form, menue=menue)
    

@app.route("/menue_create/<int:bot_id>", methods=["GET", "POST"])
@login_required
def menue_create(bot_id): 
    form = MenueForm()

    bot = BotModel.query.get(bot_id)
    if not bot or not bot.user == current_user:
        return redirect(url_for('index'))

    layouts = bot.layouts
    layout_choices = []
    for layout in layouts:
        layout_choices.append([layout.name, layout.name])
    form.layout.choices = layout_choices


    if form.validate_on_submit(): 
        layout = LayoutModel.query.filter_by(name=form.layout.data).first()
        if not layout in bot.layouts:
            return redirect(url_for("menue_create", bot_id=bot_id))
        menue = MenueModel(bot=bot, layout=layout, description=form.description.data, command=form.command.data)
        db.session.add(menue)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("menue_create.html", form=form)

@app.route("/layouts/<int:bot_id>")
@login_required
def layouts(bot_id):
    layouts = LayoutModel.query.all()
    return render_template("layouts_view.html", bot_id=bot_id, layouts=layouts)

@app.route("/layout/<int:bot_id>/<int:layout_id>")
@login_required
def layout(bot_id, layout_id):
    bot = BotModel.query.get(bot_id)
    if not bot or not bot.user == current_user:
        return redirect(url_for('index'))

    layout = LayoutModel.query.get(layout_id)

    return render_template(layout.name + ".html", layout=layout, bot=bot)


@app.route("/buy_layout/<int:bot_id>/<int:layout_id>")
@login_required
def buy_layout(bot_id, layout_id):# implement payment gateway here
    bot = BotModel.query.get(bot_id)
    if not bot or not bot.user == current_user:
        return redirect(url_for('index'))

    layout = LayoutModel.query.get(layout_id)

    if not layout in bot.layouts:
        bot.layouts.append(layout)
        db.session.commit()

    return redirect(url_for("bot", bot_id=bot.id))

   


@app.route("/viewable_objects_router/<layout_name>/<int:bot_id>/<int:menue_id>")
@login_required
def viewable_objects_router(layout_name, bot_id, menue_id):
    if layout_name == "show_products":
        return redirect(url_for("products", bot_id=bot_id, layout_name=layout_name, menue_id=menue_id))
    elif layout_name == "events":
        return redirect(url_for("events", bot_id=bot_id))
    elif layout_name == "schedule_appointment":
        return redirect(url_for("appointments", bot_id=bot_id))
    elif layout_name == "show_scheduled_times":
        return redirect(url_for("show_scheduled_times", bot_id=bot_id, layout_name=layout_name, menue_id=menue_id))

    return redirect(url_for("index")) 

@app.route("/products/<int:bot_id>/<layout_name>/<int:menue_id>", methods=["GET", "POST"])
@login_required
def products(bot_id, layout_name, menue_id):

    form = ProductsForm()

    bot = BotModel.query.get(bot_id)
    if not bot or not bot.user == current_user:
        return redirect(url_for("index"))

    layout = LayoutModel.query.filter_by(name=layout_name).first()
    if not layout or not layout in bot.layouts:
        return redirect(url_for("index"))

    menue = MenueModel.query.get(menue_id)
    if not menue or not menue.bot == bot:
        return redirect(url_for("index"))

    products = ViewableObjectModel.query.filter_by(bot_id=bot.id, layout=layout, menue=menue).all()
    products_value = []
    for product in products:
        attributes = product.attributes
        name = get_attribute(attributes, "product_name")
        price = get_attribute(attributes, "product_price")
        description = get_attribute(attributes, "product_description")
        image = get_attribute(attributes, "product_image")
        products_value.append({"name": name, "price": price, "description": description, "image": image, "id" : product.id})
    products_value.reverse()

    if form.validate_on_submit():
        product = ViewableObjectModel(layout=layout, bot=bot, menue=menue)
        name = ViewableObjectAttribute(name="product_name", value=form.name.data, viewable_object=product)
        price = ViewableObjectAttribute(name="product_price", value=str(form.price.data), viewable_object=product)
        description = ViewableObjectAttribute(name="product_description", value=form.description.data, viewable_object=product)
        image = ViewableObjectAttribute(name="product_image", value=form.image_url.data, viewable_object=product)
        db.session.add(product)
        db.session.add(name)
        db.session.add(price)
        db.session.add(description)
        db.session.add(image)
        db.session.commit()
        return redirect(url_for('products', bot_id=bot_id, layout_name=layout_name, menue_id=menue_id))

    return render_template("products.html", products_value=products_value, bot=bot, layout=layout, form=form)



@app.route("/delete_product/<int:product_id>/<int:bot_id>")
@login_required
def delete_product(product_id, bot_id):
    bot = BotModel.query.get(bot_id)
    if not bot or not bot.user == current_user:
        return redirect(url_for("index"))
    product = ViewableObjectModel.query.get(product_id)
    if product:
        if not product.bot == bot:
            return redirect(url_for("index"))
    
    layout = product.layout
    menue = product.menue
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products', layout_name=layout.name, bot_id=bot.id, menue_id=menue.id))



@app.route("/scheduled_times/<int:bot_id>/<layout_name>/<int:menue_id>", methods=["GET", "POST"])
def show_scheduled_times(bot_id, layout_name, menue_id):

    form = ScheduledTimesForm()

    bot = BotModel.query.get(bot_id)
    if not bot or not bot.user == current_user:
        return redirect(url_for("index"))

    layout = LayoutModel.query.filter_by(name=layout_name).first()
    if not layout or not layout in bot.layouts:
        return redirect(url_for("index"))

    menue = MenueModel.query.get(menue_id)
    if not menue or not menue.bot == bot:
        return redirect(url_for("index"))

    schedule_string = ""
    week = ViewableObjectModel.query.filter_by(bot_id=bot.id, layout=layout, menue=menue).first()
    
    if request.method == "GET":
        if week:
            attributes = week.attributes
            sunday = get_attribute(attributes, "sunday")
            monday = get_attribute(attributes, "monday")
            tuesday = get_attribute(attributes, "tuesday")
            wednesday = get_attribute(attributes, "wednesday")
            thursday = get_attribute(attributes, "thursday")
            friday = get_attribute(attributes, "friday")
            saturday = get_attribute(attributes, "saturday")
            schedule_string = """
            sunday:    {}\n
            monday:    {}\n
            tuesday:   {}\n
            wednesday: {}\n
            thursday:  {}\n
            friday:    {}\n
            saturday:  {}\n
            """.format(sunday, monday, tuesday, wednesday, thursday, friday, saturday)
            form.sun.data = sunday
            form.mon.data = monday
            form.tue.data = tuesday
            form.wed.data = wednesday
            form.thur.data = thursday
            form.fri.data = friday
            form.sat.data = saturday
        else:
            schedule_string = "heyyy"


    if form.validate_on_submit():
        if not week:
            week = ViewableObjectModel(layout=layout, bot=bot, menue=menue)
            days = [ViewableObjectAttribute(name="sunday", value=form.sun.data, viewable_object=week),
            ViewableObjectAttribute(name="monday", value=form.mon.data, viewable_object=week),
            ViewableObjectAttribute(name="tuesday", value=form.tue.data, viewable_object=week),
            ViewableObjectAttribute(name="wednesday", value=form.wed.data, viewable_object=week),
            ViewableObjectAttribute(name="thursday", value=form.thur.data, viewable_object=week),
            ViewableObjectAttribute(name="friday", value=form.fri.data, viewable_object=week),
            ViewableObjectAttribute(name="saturday", value=form.sat.data, viewable_object=week)]
            db.session.add(week)
            for day in days:
                db.session.add(day)
            db.session.commit()
            return redirect(url_for("show_scheduled_times", bot_id=bot_id, layout_name=layout_name, menue_id=menue_id))
        sunday = ViewableObjectAttribute.query.filter_by(name="sunday", viewable_object=week)
        monday = ViewableObjectAttribute.query.filter_by(name="monday", viewable_object=week)
        tuesday = ViewableObjectAttribute.query.filter_by(name="tuesday", viewable_object=week)
        wednesday = ViewableObjectAttribute.query.filter_by(name="wednesday", viewable_object=week)
        thursday = ViewableObjectAttribute.query.filter_by(name="thursday", viewable_object=week)
        friday = ViewableObjectAttribute.query.filter_by(name="friday", viewable_object=week)
        saturday = ViewableObjectAttribute.query.filter_by(name="saturday", viewable_object=week)
        sunday.value = form.sun.data
        monday.value = form.mon.data
        tuesday.value = form.tue.data
        wednesday.value = form.wed.data
        thursday.value = form.thur.data
        friday.value = form.fri.data
        saturday.value = form.sat.data
        db.session.commit()
        return redirect(url_for("show_scheduled_times", bot_id=bot_id, layout_name=layout_name, menue_id=menue_id))


    return render_template("scheduled_times.html", schedule_string=schedule_string, form=form)

# add delete to everything that's creatable like bots and add update also

@app.route("/admin")
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    layouts = LayoutModel.query.all()
    available_channels = ChannelModel.query.filter_by(bot=None)
    waiting_bots = BotModel.query.filter_by(channel=None)
    admins = User.query.filter_by(is_admin=True)
    
    return render_template("admin.html", layouts=layouts, available_channels=available_channels, waiting_bots=waiting_bots, admins=admins)

@app.route('/admin_users')
@login_required
def admin_users():
    users = User.query.all()
    return render_template("admin_users.html", users=users)

@app.route('/admin_promote_user/<int:user_id>')
@login_required
def admin_promote_user(user_id):
    user = User.query.get(user_id)
    user.is_admin = True
    db.session.commit()
    return redirect(url_for("admin_users"))

@app.route('/admin_delete_user/<int:user_id>')
@login_required
def admin_delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("admin_users"))


@app.route("/admin_bots")
@login_required
def admin_bots():
    if not current_user.is_admin:
        return redirect(url_for("index"))
    bots = BotModel.query.all()
    return render_template("admin_bots.html", bots=bots)

@app.route("/admin_bot/<int:bot_id>")
def admin_bot(bot_id):
    if not current_user.is_admin:
        return redirect(url_for("index"))
    bot = BotModel.query.get(bot_id)
    return render_template("admin_bot.html", bots=bots)

# def admin_channels
@app.route("/admin_channels", methods=['GET', 'POST'])
@login_required
def admin_channels():
    form = ChannelForm()

    if not current_user.is_admin:
        return redirect(url_for("index"))

    if form.validate_on_submit():
        channel = ChannelModel(channelObj_id=form.channelObj_id.data, phone_number=form.number.data)
        db.session.add(channel)
        db.session.commit()
        # webhook_request_dict = {
        # "events": ["message.created", "message.updated"], # i guess message.updated is when a message turns from pending to read and like that
        # "channelId": channel.channelObj_id,
        # "url": request.url_root + webhook_route
        # }
        # client.conversation_create_webhook(webhook_request_dict)
        return redirect(url_for("admin_channels"))

    channels = ChannelModel.query.all()
    return render_template('admin_channels.html', channels=channels, form=form)


@app.route("/admin_channel/<int:channel_id>")
@login_required
def admin_channel(channel_id):
    if not current_user.is_admin:
        return redirect(url_for("index"))

    channels = ChannelModel.query.get(channel_id)
    return render_template('admin_channel.html', channels=channels)


@app.route("/admin_layouts", methods=['GET', 'POST'])
@login_required
def admin_layouts():
    form = LayoutForm()

    if not current_user.is_admin:
        return redirect(url_for("index"))

    if form.validate_on_submit():
        layout = LayoutModel(name=form.name.data)
        db.session.add(layout)
        db.session.commit()
        return redirect(url_for("admin_layouts"))

    layouts = LayoutModel.query.all()
    return render_template('admin_layouts.html', layouts=layouts, form=form)


@app.route("/admin_linker", methods=['GET', 'POST'])
@login_required
def admin_linker():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    available_channels = ChannelModel.query.filter_by(bot=None)
    waiting_bots = BotModel.query.filter_by(channel=None)

    form = Bot_channel_linkerForm()
    bot_choices = []
    for bot in waiting_bots:
        bot_choices.append([str(bot.id), bot.name])
    form.bots.choices = bot_choices
    channel_choices = []
    for channel in available_channels:
        channel_choices.append([str(channel.id), "{}::{}".format(channel.phone_number, channel.channelObj_id)])

    form.channels.choices = channel_choices

    if form.validate_on_submit():
        bot = BotModel.query.get(int(form.bots.data))
        channel = ChannelModel.query.get(int(form.channels.data))
        bot.channel = channel
        bot.active = True
        bot.number = channel.phone_number
        db.session.commit()
        return redirect(url_for("admin"))


    return render_template("admin_linker.html", form=form)


@app.route("/delete_bot/<int:bot_id>")
@login_required
def admin_delete_bot(bot_id):
    bot = BotModel.query.get(bot_id)
    if not current_user.is_admin:
        return redirect(url_for("index"))
    
    db.session.delete(bot)
    db.session.commit()
    return redirect(url_for('admin_bots'))


@app.route("/delete_channel/<int:channel_id>")
@login_required
def admin_delete_channel(channel_id):
    channel = ChannelModel.query.get(channel_id)
    if not current_user.is_admin:
        return redirect(url_for("index"))
    
    if channel.bot:
        channel.bot.active = False
    db.session.delete(channel)
    db.session.commit()
    return redirect(url_for('admin_channels'))


@app.route("/foo")
def test():
    return render_template("test.html")