from flask import Flask, render_template, redirect, url_for
from sqlmodel import create_engine 
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv
from models import (
   BaseModel, 
   User, 
   UserSkill, 
   Friend, 
   Category, 
   Skill, 
   Tag, 
   TopicTag, 
   Topic, 
   Reply
) 
import os

load_dotenv('.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
BaseModel.set_engine(db_engine)


@app.route('/')
def index():
    pass

@app.route('/register')
def register():
    pass

@app.route('/register/next/<step>', methods=['GET', 'POST'])
def next():
    pass

@app.route('/registration/completed')
def registration_completed():
    pass


@app.route('/signin')
def signin():
    pass

@app.route('/forum')
def forum():
    topic = Topic()
    return render_template(
        'forum.html', 
        title='Forum', 
        forum = topic.get_forum(), 
        categories = Category.get_categories(),
        tags = Tag.get_all_tags()
    )

@app.route('/t/<topic_id>')
def topic(topic_id):
    topic = Topic()
    topic = topic.get_topic(topic_id)
    Topic.increase_view_count(topic_id) 
    print(topic[0]['topic'][0]['Category'].category_id)
    return render_template(
        'topic.html',
        title = 'Topic',
        topic = topic[0]['topic'][0],
        replies = topic[0]['replies'],
        category = Category.get_category(topic[0]['topic'][0]['Category'].category_id),
        categories = Category.get_categories(),
        tags = Tag.get_all_tags()
    )

@app.route('/forum/topic', methods=['POST'])
def add_topic():
    pass

@app.route('/t/<topic_id>/reply/', methods=['GET', 'POST'])
def reply():
    pass

@app.route('/t/like')
def like_topic():
    #if a user is logged in let them like the post
    pass

@app.route('/r/like')
def like_reply():
    pass

@app.route('/c/<category_name>')
def category():
    pass

@app.route('/tags/<tag_name>')
def tags(tag_name):
    pass

@app.route('/dev/<user_id>')
def user_profile():
    pass

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    pass

@app.route('/signout')
def signout():
    pass

if __name__ == '__main__':
    app.run(debug=True)