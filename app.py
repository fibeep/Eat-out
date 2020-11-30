from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import jinja2
import os
from pprint import PrettyPrinter
from random import randint

# SETUP

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/eat-out-database"
mongo = PyMongo(app)

@app.route('/')
def rest_list():
    """Displays the homepage."""

    rest_data = mongo.db.rest.find({})
    print(rest_data)
 
    context = {
        'restaurants' : rest_data
    }
    return render_template('rest_list.html', **context)


@app.route('/create_rest', methods=['GET', 'POST'])
def create_rest():
    if request.method == 'POST':
        
        new_rest = {
            'name' : request.form.get('restaurant_name'),
            'type' : request.form.get('type')
        }

        insert_result = mongo.db.restaurants.insert_one(new_rest)

        return redirect(url_for('detail', rest_id=insert_result.inserted_id))
    else:
        return render_template('create_rest.html')

@app.route('/restaurant/<rest_id>')
def detail(rest_id):
    
    rest_to_show = mongo.db.restaurants.find_one({'_id' : ObjectId(rest_id)})

    restaurant = {
        'name': rest_to_show['name'],
        'type' : rest_to_show['type'],
        'id' : str(rest_to_show['_id'])
    }

    opinions = mongo.db.opinions.find({'rest_id' : rest_id})
    rest_opinions = []
    for opinion in opinions:
        rest_opinions.append({
            'name' : opinion['name'],
            'opinion' : opinion['opinion']
        })

    context = {
        'restaurant': restaurant,
        'opinions' : rest_opinions
    }

    return render_template('detail.html', **context)

@app.route('/opinion/<rest_id>', methods=['POST'])
def opinion(rest_id):

    new_opinion = {
        'name' : request.form.get('user_name'),
        'opinion' : request.form.get('opinion')
    }

    mongo.db.opinions.insert_one(new_opinion)

    return redirect(url_for('detail', rest_id=rest_id))

@app.route('/delete/<rest_id>', methods=['POST'])
def delete(rest_id):
    mongo.db.restaurants.delete_one({'_id' : ObjectId(rest_id)})
    mongo.db.opinions.delete_many({'rest_id' : rest_id})
    return redirect(url_for('rest_list'))
# @app.route('/create_group', methods=['GET', 'POST'])
# def create_group():
#     if request.method == 'POST':
#         # Get new group leader's name 
#         new_group = {

#         }

#         # Create 

if __name__ == '__main__':
    app.run(debug=True)
