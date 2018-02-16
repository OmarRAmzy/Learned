import sqlite3

from flask import Flask , redirect ,render_template ,request ,url_for

from database_setup import Base , Restaurant , MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#create session and connect to DB
engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker (bind=engine)
session = DBSession()

conn = sqlite3.connect('restaurantmenu.db')

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants')
def Restaurants():
    restaurants = session.query(Restaurant).all()
  #  restaurants= conn.execute("Select * from Restaurant")
    return render_template('Restaurants.html' , Restaurants=restaurants )

# @app.route('/resturants')
# def get_resturants():
#
#     resturatnts = session.query(Restaurant).all()
#     output = ''
#     for i in resturatnts:
#         output += '<html> <body> <h1> '
#         output += i.name
#         output += ' </h1>'
#         output += '</body> </html>'
#
#     return output


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

@app.route('/Restaurantitems/<int:rest_id>/')
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


# @app.route('/restaurants/<int:res_id>/new/')
# def newMenuItem (res_id):
#     F = MenuItem(name = 'White Chocalate Cake', description='Black & white Chocalte' , price='$2.5' , restaurant_id=1 )
#     session.add(F)
#     session.commit()
#     session.query(MenuItem).all
#     return "New Item Added"



@app.route('/items/<int:rest_id>/')
def restaurantMenu (rest_id):
    restaurant = session.query(Restaurant).filter_by(id = rest_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id =rest_id)

    return render_template('Menu.html' , Restaurant = restaurant , items = items)


@app.route('/restaurant/<int:rest_id>/new', methods = ['GET' , 'POST'])
def newMenuItem(rest_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'] , description= request.form['description']
                           , restaurant_id=rest_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu' , rest_id = rest_id))
    else:
        return render_template('newMenuItem.html' , rest_id = rest_id)

@app.route('/Restaurants/new' , methods=['GET' , 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name = request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('Restaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/Restaurants/<int:rest_id>/delete' , methods = ['POST' , 'GET'])
def deleteRestaurant(rest_id):
    restaurant = session.query(Restaurant).filter_by(id=rest_id).one()
    session.delete(restaurant)
    session.commit()

    return redirect(url_for('Restaurants'))

@app.route('/restaurant/<int:rest_id>/<int:menu_id>/edit/')
def editMenuItem(rest_id , menu_id):
    return


@app.route('/restaurant/<int:rest_id>/<int:menu_id>/delete/')
def deleteMenuItem(rest_id , menu_id):
    return



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0' , port=5000)