from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

MyFirstRestaurant = Restaurant(name='Pizza Place'  )
session.add(MyFirstRestaurant)
session.commit()
session.query(Restaurant).all()

name = "feter"
desc = "Sogok"
price = "$ 4"


F = MenuItem(name = name , description=desc , price =price ,
                  restaurant=MyFirstRestaurant)
session.add(F)
session.commit()
session.query(MenuItem).all()

#cheesepizza = MenuItem( name="Cheese Pizaa", description="Sh mozarrela"
#                      , price="$ 8.8", restaurant=MyFirstRestaurant)
#session.add(cheesepizza)
#session.commit()
#session.query(MenuItem).all()

#firstResult = session.query(Restaurant).first()
#print firstResult.id

#restaurant_2 = Restaurant(name='Sabry Place'  )
#session.add(restaurant_2)
#session.commit()
#session.query(Restaurant).all()



AllRestaurants = session.query(Restaurant).all()
AllItems = session.query(MenuItem).all()



for r in AllRestaurants:
    print r.id , " " , r.name

print "\n"

for item in AllItems:
  print item.id , " " , item.name , item.restaurant.name , item.restaurant.id


#Update = session.query(MenuItem).filter_by(id=1).one()
#Update.name = "Burger egg"
#session.add(Update)
#session.commit()


