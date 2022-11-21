from flask import Flask, jsonify, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from flask_marshmallow import Marshmallow
from datetime import datetime
from sqlalchemy.orm import Session
from config import _SQLALCHEMY_DATABASE_URI


# Instantiate Flask App object
app = Flask(__name__)

# configurations for flask app 
app.config['SQLALCHEMY_DATABASE_URI'] = _SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# instantiate SQLAlchemy and Marshmallow class object 
db = SQLAlchemy(app)
ma = Marshmallow(app)


Base = automap_base()
engine = create_engine(_SQLALCHEMY_DATABASE_URI)

Base.prepare(autoload_with=engine)

Meeting = Base.classes.meetings
Event = Base.classes.events
News =  Base.classes.news


# define marshmallow schema classes
class MeetingSchema(ma.Schema):
    class Meta:
        fields = ('Date', 'Time', 'Location', 'Groups', 'Type', 'Info')

class EventSchema(ma.Schema):
    class Meta:
        fields = ('Date', 'Location','Desc', 'Time', 'Event')    

class NewsSchema(ma.Schema):
    class Meta:
        fields = ('Date', 'Desc', 'Read_more', 'Title')    

# instantiate marshmallow schema class 
meeting_schema = MeetingSchema()
meetings_schema = MeetingSchema(many=True)

event_schema = EventSchema()
events_schema = EventSchema(many=True)

news_schema = NewsSchema(many=True)

# return list of the next 5 upcoming meetings
def get_upcoming_meetings():
    today = datetime.today().strftime('%Y-%m-%d')
    upcoming_meetings = db.session.query(Meeting).filter(Meeting.Date >= today).limit(15).all()
    result = meetings_schema.dump(upcoming_meetings)
    return result

# return list of 
def get_upcoming_events():
    today = datetime.today().strftime('%Y-%m-%d')
    upcoming_events = db.session.query(Event).filter(Event.Date >= today).limit(30).all()
    result = events_schema.dump(upcoming_events)
    return result

def get_police_news():
    latest_news =  db.session.query(News).limit(10).all()
    result = news_schema.dump(latest_news)
    return result


# define app routes and endpoints
# home route serves html page with upcoming meetings and upcoming activities

def home():
    months = {'01':'JAN', '02':'FEB', '03':'MAR', '04':'APR', '05':'MAY', 
    '06':'JUN', '07':'JUL', '08':'AUG', '09':'SEP', '10':'OCT', '11':'NOV', '12':'DEC'}
    upcoming_meetings = get_upcoming_meetings()
    upcoming_events = get_upcoming_events()
    police_news = get_police_news()
    return render_template(
        'home.html', 
        upcoming_events=upcoming_events,
        upcoming_meetings=upcoming_meetings,
        police_news=police_news,
        months=months
    )

def index():
    user_agent = request.headers.get('User-Agent') 
    return '<p>Your browser is {}</p>'.format(user_agent)

# api endpoint returns json object of all meetings in database 
@app.route('/api_v1/meetings', methods=['GET'])
def meetings():
   all_meetings = db.session.query(Meeting).all()
   result = meetings_schema.dump(all_meetings)
   return jsonify(result), 200


# api endpoint returns json obeject of next 5 meetings based on current date
@app.route('/api_v1/upcoming_meetings', methods=['GET'])
def upcoming_meetings():
    result = get_upcoming_meetings()
    return jsonify(result), 200


# api endpoint returns json object of upcoming 5 library events based on today's date
@app.route('/api_v1/events', methods=['GET'])
def events():
    all_events = db.session.query(Event).all()
    result = events_schema.dump(all_events)
    return jsonify(result), 200


# api endpoint returns json object of activities in database
@app.route('/api_v1/upcoming_events', methods=['GET'])
def upcoming_events():
    result = get_upcoming_events()
    return jsonify(result), 200

# api endpoint returns
@app.route('/api_v1/police_news', methods=['GET'])
def latest_news():
    result = get_police_news()
    return jsonify(result), 200


app.add_url_rule('/', 'home', home)
app.add_url_rule('/user-agent', view_func=index)

if __name__ == '__main__':
    app.run(debug=True)

