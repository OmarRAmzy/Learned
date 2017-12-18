from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
#import CRUD Operations from lesson 1
import StringIO
from database_setup import Base , Restaurant , MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#create session and connect to DB
engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker (bind=engine)
session = DBSession()


class webserverHandler (BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html> <body>"
                output += "<h1> Make a New Restaurant </h1> "
                output += "<form method ='POST' enctype = 'multipart/form-data'" \
                          "action = 'restaurants/new' >"
                output += "<input type ='text' name='newRestaurantName' placeholder" \
                         "='New Restaurant Name' >"
                output += "<input type = 'submit' value = 'Create' >"
                output += "</body> </html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                restaurantIDPath= self.path.split("/")[2]
                MyRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if MyRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type' , 'text/html')
                    self.end_headers()
                    output = "<html> <body>"
                    output += "<h1>"
            #        output += str (MyRestaurantQuery.id)
                    output += "</h1>"
                    output += "<form method = 'POST'enctype='multipart/form-data'" \
                              "action ='/restaurant/%s/edit' >"% restaurantIDPath
                    output+= " <input name = 'newRestaurantName' type='text' placeholder =" \
                             "'%s' > " % MyRestaurantQuery.name
                    output += "<input type = 'submit' value ='Rename' >"
                    output += "</form>"
                    output += "</body> </html>"
                    self.wfile.write(output)

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                MyRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if MyRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html> <body>"
                    output += "<h1>"
                    output += " Are you want to Delete Restaurant with name:  "
                    output += MyRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method = 'POST'enctype='multipart/form-data'" \
                              "action ='/restaurant/%s/delete' >" % restaurantIDPath
                    output += "<input type = 'submit' value ='Delete' >"
                    output += "</form>"
                    output += "</body> </html>"
                    self.wfile.write(output)

            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()

                self.send_response(200)
                self.send_header('Content-type' , 'text/html')
                self.end_headers()
                output = ""
                output += "<html> <body>"
                output += "<a href = 'restaurants/new'> Make a new Restaurant  " \
                          "Here </a> </br> </br>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href = ' /restaurant/%s/edit'> Edit </a> " % restaurant.id
                    output += "</br>"
                    output += "<a href = ' /restaurant/%s/delete'> Delete </a> " %restaurant.id
                    output += "</br> </br>"

                output += "</body> </html>"
                self.wfile.write(output)
                return


            if self.path.endswith("/Hello"):
                self.send_response(200)
                self.send_header('contact-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html> <body> <h1> Hello! <h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action ='/Hello' " \
                          "> <h2> what would you like me to say? </h2> <input name ='message' " \
                          "type = 'text'> <input type = 'submit' value = 'Submit'>  </form>"
                output += " </body> </html> "
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/Hola"):
                self.send_response(200)
                self.send_header('contact-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html> <body> <h1> Hola! </h1>  " \
                          "<a href = '\Hello'> Back to Hello </a> "
                output += "<form method = 'POST' enctype='multipart/form-data' action ='/Hello' " \
                          "> <h2> what would you like me to say? </h2> <input name ='message' " \
                          "type = 'text'> <input type = 'submit' value = 'Submit'>  </form>"
                output += " </body> </html> "


                self.wfile.write(output)
                print output
                return

        except IOError:
                self.send_error(404, "File Not Found %s" % self.path)
    def do_POST(self):
        try:
            if self.path.endswith("edit"):
                 ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                 if ctype == 'multipart/form-data':
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        messagecontent = fields.get('newRestaurantName')
                        restaurantIDPath = self.path.split("/")[2]

                        myRestaurantQuery = session.query(Restaurant).filter_by(id =restaurantIDPath).one()
                        if myRestaurantQuery != []:
                            myRestaurantQuery.name = messagecontent[0]
                            session.add(myRestaurantQuery)
                            session.commit()
                            self.send_response(301)
                            self.send_header('Content-type', 'text/html')
                            self.send_header('Location', '/restaurants')
                            self.end_headers()
                            return

            if self.path.endswith("delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                restaurantIDPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery != []:
                        session.delete(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                        return


            if self.path.endswith("restaurants/new"):
                 ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                 if ctype == 'multipart/form-data' :
                      fields = cgi.parse_multipart(self.rfile , pdict)
                      messagecontent = fields.get('newRestaurantName')

            newRestaurant = Restaurant(name = messagecontent[0])
            print messagecontent[0]
            session.add(newRestaurant)
            session.commit()
            self.send_response(301)
            self.send_header('Content-type' , 'text/html')
            self.send_header('Location' , '/restaurants')
            self.end_headers()
            return

        except:
           pass



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "web server running on port %s " % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered , stopping webserver..."
        server.socket.close()


if __name__ == '__main__':
    main()
