import sqlite3

conn = sqlite3.connect("restaurantmenu.db")
c = conn.cursor()
#c.execute('''
#          CREATE TABLE restaurnt
#          (id INTEGER PRIMARY KEY ASC NOT NULL ,
#          name VARCHAR(250) NOT NULL )
#          ''')

#c.execute('''
#          CREATE TABLE menu_item
#          (id INTEGER PRIMARY KEY ASC NOT NULL ,
#          name VARCHAR(250) , price VARCHAR(250) ,
#          description VARCHAR(250) NOT NULL , restaurant_id INTEGER NOT NULL,
#            FOREIGN KEY ( restaurant_id) REFERENCES restaurant(id) )
#          ''')

#for i in range(2 , 20):
#c.execute("DELETE FROM restaurant WHERE id = 1 ; ")
#c.execute("DELETE FROM menu_item WHERE id = 1 ; ")

print "Record deleted"

print " Table Edited sucessfully "

conn.commit()
conn.close()