from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired, length, Email
from wtforms_components import SelectField
from flask_wtf.file import FileField, FileAllowed 
from wtforms.widgets import TextArea


class RegisterForm(FlaskForm):
    email = wtforms.StringField("الايميل", validators=[length(min=3, max=255), Email()])
    full_name = wtforms.StringField("الاسم الكامل", validators=[length(max=255), DataRequired()])
    password = wtforms.StringField("الرقم السري", validators=[length(min=7, max=50)])
    username = wtforms.StringField("السم المستخدم", validators=[DataRequired(), length(min=4, max=60)])
    number = wtforms.StringField("رقم الجوال", validators=[DataRequired(), length(max=20)]) # validate with messagebird
    submit = wtforms.SubmitField("سجل")

class LoginForm(FlaskForm):
    username = wtforms.StringField("اسم المستخدم",  validators=[DataRequired()])
    password = wtforms.StringField("الرقم السري")
    submit = wtforms.SubmitField("تسجيل الدخول")



class BotForm(FlaskForm):
    name = wtforms.StringField("اسم البوت",  validators=[DataRequired(), length(max=255)])
    number = wtforms.StringField("رقم الجوال المراد للبوت", validators=[DataRequired(), length(max=20)])
    submit = wtforms.SubmitField("اطلب بوت")

layouts = (
    ("show_products", "نظام عرض المنتجات/الخدمات"),
    ("schedule_appointment", "نظام عرض وحجز المواعيد"),
    ("events", "نظام عرض والتسجيل في الفعاليات"),
)

class MenueForm(FlaskForm): 
    command = wtforms.StringField("اسم الامر",  validators=[DataRequired(), length(max=20)])
    description = wtforms.StringField("وصف الامر",  validators=[DataRequired(), length(max=150)])
    layout = SelectField("النظام المتبع", choices=layouts, validators=[DataRequired()])
    submit = wtforms.SubmitField("انشئ امر جديد")

class ProductsForm(FlaskForm): # process form
    name = wtforms.StringField("الاسم",  validators=[DataRequired(), length(max=255)])
    price = wtforms.FloatField("السعر",  validators=[DataRequired()])
    description =  wtforms.StringField("الوصف", validators=[length(max=500)])
    submit = wtforms.SubmitField("ارفع منتج")

class ChannelForm(FlaskForm): # admin form
    channelObj_id = wtforms.StringField("معرف القناة",  validators=[DataRequired(), length(max=50)])
    number = wtforms.StringField("رقم جوال القناة",  validators=[DataRequired(), length(max=20)])
    submit = wtforms.SubmitField("انشئ قناة")


class LayoutForm(FlaskForm): # admin form
    name = wtforms.StringField("اسم التنسيق",  validators=[DataRequired()])
    submit = wtforms.SubmitField("انشئ امر جديد")

languages = (
    ("ar", "العربية"),
    ("en", "English")
)

class LanguageForm(FlaskForm):
    language = SelectField("select language", choices=languages, validators=[DataRequired()])



class Bot_channel_linkerForm(FlaskForm):
    bots = SelectField("select bot", choices=languages, validators=[DataRequired()])
    channels = SelectField("select channel", choices=languages, validators=[DataRequired()])
    submit = wtforms.SubmitField("اربط")