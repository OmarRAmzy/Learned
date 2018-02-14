from flask import Flask , redirect ,render_template ,request ,url_for

from database_setup import Base , Restaurant , MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#create session and connect to DB
engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker (bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
@app.route('/resturants')
def get_resturants():
    
    resturatnts = session.query(Restaurant).all()
    output = ''
    for i in resturatnts:
        output += '<html> <body> <h1> '
        output += i.name
        output += ' </h1>'
        output += '</body> </html>'

    return output


@app.route('/items')
def get_items ():
    resturatnts = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id =resturatnts.id)
    output= ''
    for i in items:
        output+='<html> <body> <h1> '
        output += i.name
        output+=' </h1>'
        output+= i.price
        output += '</br>'
        output += i.description
        output += '</br> </br>'
        output+= '</body> </html>'
    return output


@app.route('/resturants/<int:res_id>/')
def get_resturant_id (res_id):
    resturatnts = session.query(Restaurant).filter_by(id =res_id)
    output = ''
    for i in resturatnts:
        output += '<html> <body> <h1> '
        output += i.name
        output += ' </h1>'
        output += '</body> </html>'

    return output

@app.route('/items/<int:rest_id>/')
def get_items_id (rest_id):
    #resturatnts = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id =rest_id)
    output= ''
    for i in items:
        output+='<html> <body> <h1> '
        output += i.name
        output+=' </h1>'
        output+= i.price
        output += '</br>'
        output += i.description
        output += '</br> </br>'
        output+= '</body> </html>'
    return output


@app.route('/restaurants/<int:res_id>/new/')
def new_menu_item (res_id):
    F = MenuItem(name = 'White Chocalate Cake', description='Black & white Chocalte' , price='$2.5' , restaurant_id=1 )
    session.add(F)
    session.commit()
    session.query(MenuItem).all
    return "New Item Added"


@app.route('/itemshtml/<int:rest_id>/')
def get_items_id_templates (rest_id):
    restaurant = session.query(Restaurant).filter_by(id = rest_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id =rest_id)

    return render_template('Menu.html' , Restaurant = restaurant , items = items)

@app.route()

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0' , port=5000)