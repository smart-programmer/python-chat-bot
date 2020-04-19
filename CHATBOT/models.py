from CHATBOT import db, login_manager
from datetime import datetime

class WebhookMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messagebird_request_string = db.Column(db.String(2000), nullable=False)
    message_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)




class ChannelModel(db.Model):# everything that's channel specific needs to have a relationship with ChannelModel
    id = db.Column(db.Integer, primary_key=True)
    channelObj_id = db.Column(db.String(50), nullable=False)
    contacts = db.relationship("ContactModel", cascade="all,delete", backref="channel")
    menues = db.relationship("MenueModel", backref="channel", cascade="all,delete")
    viewable_objects = db.relationship("ViewableObjectModel", backref="channel", cascade="all,delete")
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class ContactModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channel_model.id"), nullable=False)
    name = db.Column(db.String(255))
    session = db.relationship("ConversationSessionModel", backref="contact", uselist=False, cascade="all,delete")
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class ConversationSessionModel(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    step_counter = db.Column(db.Integer, nullable=False, default=0)
    layout_name = db.Column(db.String(15))
    conversationObj_id = db.Column(db.String(40), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact_model.id"))
    message = db.Column(db.Text, nullable=False)
    arguments = db.relationship("ConversationSessionArgModel", backref="session", cascade="all,delete") # to carry out information for layouts
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class ConversationSessionArgModel(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    argument_name = db.Column(db.String(30), nullable=False)
    argument_value = db.Column(db.String(200), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey("conversation_session_model.id"), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)



class MenueModel(db.Model): # a model that stores bot possible procedures (every customer creates there own menues)
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey("channel_model.id"), nullable=False)
    layout_name = db.Column(db.String(30), nullable=False) # this isn't a database relationship because we don't want the LayoutModel to store all customer's menues
    command = db.Column(db.String(20), nullable=False)
    descritption = db.Column(db.String(150), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
       


class LayoutModel(db.Model): # represents how a command should be treated (we create the layouts)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True) # maybe make this the primary_key
    viewable_objects = db.relationship("ViewableObjectModel", backref="layout", cascade="all,delete")
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 



class ViewableObjectModel(db.Model): # insted of creating a model for every layout like OfferModel or StaticModel or EventModel we create a ViewableObjectModel object with that layout model attributes attached to it and a tag to indicate which layout this object reoresent for example object.tag = "event" and object.attributes == (event mdoel attributes) 
    id = db.Column(db.Integer, primary_key=True) # if a layout model needs a complex attribute we can always create a new Model for it and create a one way relation where the attribute has the layout_model id but the layout_model doesn't know anything about the attrubute (just like requirements and prticipants)
    tag = db.Column(db.String(30), nullable=False) # change this tag into a relationship with the layout model
    attributes = db.relationship("ViewableObjectAttribute", backref="viewable_object", cascade="all,delete")
    channel_id = db.Column(db.Integer, db.ForeignKey("channel_model.id"), nullable=False)
    layout_id = db.Column(db.Integer, db.ForeignKey("layout_model.id"), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 



class ViewableObjectAttribute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False) 
    # value = db.relationship("ViewableObjectAttributeValue", backref="attribute", uselist=False)
    value = db.Column(db.Text, nullable=False)
    viewable_object_id = db.Column(db.Integer, db.ForeignKey("viewable_object_model.id"), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 


# class ViewableObjectAttributeValue(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     value = db.Column(db.Text, nullable=False) 
#     attribute_id = db.Column(db.Integer, db.ForeignKey("viewableobjectattribute.id"), nullable=False)
#     create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 


# processes models
# processes models are models nesesary for different processes liek registration process needs RequirementModel and ParticipantModel and ParticipantInformationModel

class RequirementModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    viewable_object_id = db.Column(db.Integer, nullable=False)
    requirement_name = db.Column(db.String(150), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class ParticipantModel():
    id = db.Column(db.Integer, primary_key=True)
    viewable_object_id = db.Column(db.Integer, nullable=False)
    information = db.relationship("ParticipantInformationModel", backref="participant", cascade="all,delete")
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class ParticipantInformationModel():
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Text, nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey("participant_model.id"), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

 

# just for good measure i'll make the models for the layouts in case i find a problem with the ViewableObjectModel system



class OfferModel():
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(60), nullable=False) 
    message = db.Column(db.String(500), nullable=False) 
    start_date = db.Column(db.String(100), nullable=False) 
    end_date = db.Column(db.String(100), nullable=False) 
    channel_id = db.Column(db.Integer, db.ForeignKey("channel_model.id"), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 


class ServiceModel():
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False) 
    price = db.Column(db.Integer, nullable=False) 
    channel_id = db.Column(db.Integer, db.ForeignKey("channel_model.id"), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class AppointmentModel(): # participtable layout which means it must have a relation with requirements and participants
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(60), nullable=False) 
    title = db.Column(db.String(500), nullable=False) 
    state = db.Column(db.String(100), nullable=False) 
    end_date = db.Column(db.String(100), nullable=False) 
    channel_id = db.Column(db.Integer, db.ForeignKey("channel_model.id"), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)





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