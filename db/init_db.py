import sqlite3 as sq
import csv 

#create database and a connection to it 
conn = sq.connect('SB_City_Info.sqlite')
cursor = conn.cursor()

#create table statements
create_mt_table = """
    CREATE TABLE meetings (
        meeting_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT,
        Groups TEXT,
        Info TEXT,
        Location TEXT,
        Time TEXT,
        Type TEXT
    );
"""

create_event_table = """
    CREATE TABLE events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT,
        Desc TEXT,
        Event TEXT,
        Location TEXT,
        Time TEXT
    );
"""

create_news_table = """
    CREATE TABLE news (
        news_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Date TEXT,
        Desc TEXT,
        Read_more TEXT,
        Title TEXT
    );
"""

# commit query
cursor.execute(create_mt_table)
cursor.execute(create_event_table)
cursor.execute(create_news_table)
conn.commit()


#populate db
#import meeting data 
reader = csv.reader(open('../data/city_meetings_clean.csv', 'r'), delimiter=',')

rowIdCount = 0 
insert_statement_meetings = "INSERT INTO meetings VALUES(Null,?,?,?,?,?,?)"

for row in reader:
    if rowIdCount:
        cursor.execute(insert_statement_meetings, row)
    rowIdCount += 1


conn.commit()

#import library events data 
reader = csv.reader(open('../data/library_events.csv', 'r'), delimiter=',')

rowIdCount = 0 
insert_statement_events = "INSERT INTO events VALUES(Null,?,?,?,?,?)"

for row in reader:
    if rowIdCount:
        cursor.execute(insert_statement_events, row)
    rowIdCount += 1

conn.commit()

# import police news
reader = csv.reader(open('../data/police_news.csv', 'r'), delimiter=',')

rowIdCount = 0 
insert_statement_news = "INSERT INTO news VALUES(Null,?,?,?,?)"

for row in reader:
    if rowIdCount:
        cursor.execute(insert_statement_news, row)
    rowIdCount += 1

conn.commit()
conn.close()