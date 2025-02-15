from flask import Flask,request
import static_msg as msgs
from dotenv import dotenv_values
from pymongo import MongoClient
from flask_cors import CORS
from auth import auth_v1
from db import get_db_mongo
from bson.json_util import dumps, loads 

config = dotenv_values(".env")

PASSWORD='CpWfPvUiBme6TZSd'
ATLAS_URI=f'mongodb+srv://zyuvrajsinh09:{PASSWORD}@startup.m8iole4.mongodb.net/?retryWrites=true&w=majority'
DB_NAME='startup'

# instead of ATLAS_URI, DB_NAME, use config['ATLAS_URI'] config['DB_NAME']
app =  Flask(__name__)
CORS(app)
#db = g._database = PyMongo(current_app).db
db=None
with app.app_context():
    db = get_db_mongo(ATLAS_URI,DB_NAME)

# def startup_db_client():
#     app.mongodb_client = MongoClient(config["ATLAS_URI"])
#     app.database = app.mongodb_client[config["DB_NAME"]]
#     print("Connected to the MongoDB database!")


# def shutdown_db_client():
#     app.mongodb_client.close()

@app.route('/',method=['GET'])
def index():
    return {'status':200, 'API_CONTRACTS':['/login','/logout','/register','/contact-us','/comments','/comments/<blog_id>','/subscription']}

@app.route('/contact-us',methods=['POST'])
def contact_us():
    if request.method == 'POST':
        name,email = request.json['name'],request.json['email']
        subject, message = request.json['subject'],request.json['message']
        contact_doc = { 'name' : name, 'email' : email , 'subject' : subject,'message' : message}
        try:
            db.contact_us.insert_one(contact_doc)
            return {'status':200,'msg':'Your request is successfully processed!'}
        except:
            return {'status':500,'msg':'Error while processing DB!'}

@app.route('/comments',methods=['GET','POST'])
def comments_handler():
    if request.method=='POST':
        name,email = request.json['name'],request.json['email']
        website, comment = request.json['website'],request.json['comment']
        blog_id = request.json['blog_id']
        comments_doc = { 'name' : name, 'email' : email , 'website' : website,'comment' : comment,'blog_id':blog_id}
        try:
            db.comments.insert_one(comment_doc)
            return {'status':200,'msg':'Your comment request is successfully processed!'}
        except:
            return {'status':500,'msg':'Error while processing DB!'}
    elif request.method=='GET':
        try:
            return {'comments':dumps(list(db.comments.find(limit=10)))}
        except:
            return {'status':404,'msg': 'Unexpected error while fetching comments'}
    else:
        return {'status':500,'msg':'Unknown type'}

@app.route('/comments/<int:blog_id>',methods=['GET'])
def comments_handler_blogs(blog_id):
    try:
        return {'comments': dumps(list(db.comments.find({'blog_id':blog_id})))}
    except:
        return {'status':'Unexpected error fetching comments for blog_id.'}
        

@app.route('/subscription')
def subscription_handler():
    if request.method=='POST':
        email = request.json['email']
        subscription_doc = {'email' : email}
        try:
            db.subscription.insert_one(subscription_doc)
            return {'status':200,'msg':'The email is registered with us!'}
        except:
            return {'status':500,'msg':'Error while processing DB for Subscription!'}
        # take email and store in database


    
if __name__=='__main__':
    app.register_blueprint(auth_v1)
    app.config['DEBUG'] = True
    app.config['MONGO_URI'] = ATLAS_URI
    app.run()