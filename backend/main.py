from flask import Flask,request
import static_msg as msgs

app =  Flask(__name__)

@app.route('/contact-us',methods=['POST'])
def contact_us():
    if request.method == 'POST':
        name,email = request.json['name'],request.json['email']
        subject, message = request.json['subject'],request.json['message']

        return {'status':200,'msg':'Your request is successfully processed!'}

@app.route('/comments',methods=['GET','POST'])
def comments_handler():
    if request.method=='POST':
        name,email = request.json['name'],request.json['email']
        website, comment = request.json['website'],request.json['comment']
        return 'The comment is updated successfully'
    elif request.method=='GET':
        return msgs.comments
    else:
        return {'status':500,'msg':'Unknown type'}

@app.route('/subscription')
def subscription_handler():
    if request.method=='POST':
        # take email and store in database
        return {'status': 200, 'msg':'the email is registered with us'}


    
if __name__=='__main__':
    app.run()