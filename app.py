from flask import Flask, jsonify, request, render_template
from datos_dummy import books
import pymongo
import json

with open('books.json','r') as r:
    data = json.load(r)


#mongo credencial
url = 'mongodb+srv://user:newpassword@cluster0.0spamm9.mongodb.net/?retryWrites=true&w=majority'
myclient = pymongo.MongoClient(url, 27017)
mydb = myclient["Cluster0"]
books = mydb['books']
# Debo empezarla afuera 
# ...

app = Flask(__name__)
app.config["DEBUG"] = True


#pages
@app.route('/')
def index():
    return render_template('index.html')

# all books
@app.route('/books/all', methods=['GET'])
def all():

    filter = {}
    projection = {'_id':0}
    all = list(books.find(filter=filter, projection=projection))
    lista = []
    for i in all:
        title = i.get("title", "none")
        lista.append(title)
    return render_template("all.html", all=lista)

# 1.Ruta para obtener todos los libros
@app.route('/books/id', methods=['GET', 'POST'])
def createid():
    if request.method == 'POST':
        id = int(request.form['id'])
        
        
        filter = {'id': id}
        projection = {'_id': 0}
        all_books = list(books.find(filter=filter, projection=projection))
        # all_books = jsonify(all_books)
        lista = []

        
        if not all_books:
            return render_template("index.html", todos="No books found for this ID")
        
        for i in all_books:

            title = i.get("title", "none")
            lista.append(title)

        return render_template("createid.html", all=lista)

      
    return render_template("createid.html", todos="N/A")



# pedir libro por id 
@app.route('/api/v0/resources/book', methods=['GET'])
def book_id(): 
    if 'id' in request.args:
        id = int(request.args['id'])
        filter = {"id": id}
        projection = {'_id': 0}
        all = list(books.find(filter=filter, projection=projection))
        if all == []:
            return "Book not found with the id requested"    
        else:
            return all

    else:
        return "No id provided"

@app.route('/about/')
def about():
    return render_template('about.html')

# pedir libro por id 
# @app.route('/api/v0/resources/book', methods=['GET'])
# def book_id(): 
#     if 'id' in request.args:
#         id = int(request.args['id'])
#         filter = {"id": id}
#         projection = {'_id': 0}
#         all = list(books.find(filter=filter, projection=projection))
#         if all == []:
#             return "Book not found with the id requested"    
#         else:
#             return all

#     else:
#         return "No range provided"



# pedir librocon titulo
@app.route('/api/v0/resources/booktitle/<string:title>', methods=['GET'])
def book_title(title):
    if 'title' in request.args:
        title = str(request.args['title'])
        filter = {"title": title}
        projection = {'_id': 0}
        all = list(books.find(filter=filter, projection=projection))
        if all == []:
            return "Book not found with the title requested"    
        else:
            return all
    else:
        return "No title provided"





@app.route('/api/v1/resources/booktitle', methods=['GET'])
def book_title_nv1():

    title = request.get_json()['title'] # coge datos del body
    filter = {"title": title}
    projection = {'_id': 0}
    all = list(books.find(filter=filter, projection=projection))
    if all == []:
        return "Book not found with the title requested"    
    else:
        return all



# by body
# @app.route('/api/v1/resources/book/add', methods=['POST'])
# def book_title_body_2():
#     results = []
#     libro = request.get_json()
#     books.insert_one(libro)
#     filters = {}
#     projections = {"_id":0}
#     results = list(books.find(filter=filters, projection=projections))

#     if results != []:
#         return jsonify(results)
#     else:
#         return "Book title not found" 




# pedir libros por rango
@app.route('/api/v0/resources/bookrange', methods=['GET'])
def book_range():
    
    if ('id' in request.args) & ('id' in request.args):
        start = int(request.args['id'])
        end = int(request.args['id'])
        filter = {"id": {'$gte': start, '$lte': end}}
        projection = {'_id': 0}
        all = list(books.find(filter=filter, projection=projection))
        if all == []:
            return "Book not found with the id requested"    
        else:
            return all

    else:
        return "No range provided"
    

# delete libros - funciona en postman
@app.route('/api/v1/resources/book/delete', methods=['DELETE'])
def delete_book():
    
    if 'title' in request.args:
        titulo = str(request.args['title'])
        
        filter = {"title": titulo}
        projection = {'_id': 0}
        delete_result = books.delete_one(filter=filter)
        if delete_result.deleted_count == 0:
            return "Book not found with the title requested"
        else:
            return "Successfully deleted"

    else:
        return "No range provided"


# update published year
# @app.route('/api/v1/resources/book_published_year_update', methods=['UPDATE'])
# def update_year_book():
    
#     if ('id' in request.args) and ('published' in request.args):
#         id = str(request.args['id'])
#         published = str(request.args["published"])
#         filter = ({"id": id}, {'$set': {'published': published}}})
#         projection = {'_id': 0}
#         update_result = books.delete_one(filter=filter)
#         if update_result.matchedCount == 0:
#             return "Book not found with the title requested"
#         else:
#             return "Successfully deleted"

#     else:
#         return "No range provided"
    
if __name__ == "__main__":
	app.run(debug=True, port=8080)