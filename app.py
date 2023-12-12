from flask import Flask, jsonify, request
from datos_dummy import books
import pymongo
import json

app = Flask(__name__)
app.config["DEBUG"] = True

# with open('books.json', 'w') as file:
#     json.dump(books, file)

with open('books.json','r') as r:
    data = json.load(r)

url = 'mongodb+srv://user:newpassword@cluster0.zwsgeaa.mongodb.net/?retryWrites=true&w=majority'
myclient = pymongo.MongoClient(url)

mydb = myclient["Cluster0"]
books = mydb['data']
books.insert_many(data)



@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"



# 1.Ruta para obtener todos los libros
@app.route('/api/v0/resources/books/all', methods=['GET'])
def get_all():
    filter = {}
    projection = {'_id':0}
    all = list(books.find(filter=filter, projection=projection))
    return all



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




@app.route('/api/v1/resources/book/add', methods=['POST'])
def book_title_body_2():
    results = []
    libro = request.get_json()
    books.insert_one(libro)
    filters = {}
    projections = {"_id":0}
    results = list(books.find(filter=filters, projection=projections))

    if results != []:
        return jsonify(results)
    else:
        return "Book title not found" 








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
	app.run()