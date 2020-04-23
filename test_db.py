from CHATBOT.models import *

db.drop_all()
db.create_all()

# create user

c = ChannelModel(channelObj_id="7e4da85010004d32a1427e4a2edcee33")
db.session.add(c)

# create user

l = LayoutModel(name="show_products_prices")
db.session.add(l)
m = MenueModel(command="show me products", layout_name="show_products_prices", description="our products and prices", channel=c)
db.session.add(m)


v1 = ViewableObjectModel(channel=c, layout_name=l.name)
v1t1 = ViewableObjectAttribute(name="product_name", value="Playstation 5", viewable_object=v1)
v1t2 = ViewableObjectAttribute(name="product_price", value="1800", viewable_object=v1)
db.session.add(v1)
db.session.add(v1t1)
db.session.add(v1t2)
v2 = ViewableObjectModel(channel=c, layout_name=l.name)
v2t1 = ViewableObjectAttribute(name="product_name", value="Xbox scorpio", viewable_object=v2)
v2t2 = ViewableObjectAttribute(name="product_price", value="1900", viewable_object=v2)
db.session.add(v2)
db.session.add(v2t1)
db.session.add(v2t2)
v3 = ViewableObjectModel(channel=c, layout_name=l.name)
v3t1 = ViewableObjectAttribute(name="product_name", value="Nintendo switch", viewable_object=v3)
v3t2 = ViewableObjectAttribute(name="product_price", value="1100", viewable_object=v3)
db.session.add(v3)
db.session.add(v3t1)
db.session.add(v3t2)
v4 = ViewableObjectModel(channel=c, layout_name=l.name)
v4t1 = ViewableObjectAttribute(name="product_name", value="pre build gaming pc", viewable_object=v4)
v4t2 = ViewableObjectAttribute(name="product_price", value="3000", viewable_object=v4)
db.session.add(v4)
db.session.add(v4t1)
db.session.add(v4t2)




db.session.commit()