import scrapy
import json
from sb_city_scraper.items import LibraryEvent
from datetime import datetime


# following two functions are meant for data cleansing
# remove html tags and new line characters in text
# @param str
# @return str 
def process_text(text):
    spChars = ['\n', '<p>', '</p>']
    for char in spChars:
        text = text.replace(char, '')
    return text


# return 12 hour time format
# @param str
# @return str
def process_time(time):
    time_period = ''
    time_arr =  time.split(':')

    if int(time_arr[0]) >= 12:
        if int(time_arr[0]) == 12:
            pass
        else:
            time_arr[0] = int(time_arr[0]) - 12
        time_period = 'PM'
    else:
        if int(time_arr[0] == 0):
            time_arr[0] = 12
        time_period = 'AM'

    result = str(time_arr[0]) + ':' + time_arr[1] + ' ' + str(time_period)
    return result


class LibraryEventsSpider(scrapy.Spider):

    name = 'library_events'
    allowed_domains = ['teamup.com']

    # construct api request based on today's date
    today = datetime.today().strftime('%Y-%m-%d')
    start_urls = ['https://teamup.com/ksv46dap1xst4izsqv/events?startDate={}&endDate=2023-06-30&tz=America/Los_Angeles'.format(today)]

    def parse(self, response):
        # load api json response 
        resp = json.loads(response.body)
        events = resp.get('events')

        # for loop constructing ind LibraryEvent objects 
        for event in events:
            
            library_event = LibraryEvent()
            library_event['Event'] = event.get('title')

            # clean locations string
            clean_location = process_text(event.get('location'))
            library_event['Location'] = clean_location
            date_time = event.get('start_dt')

            # try creating datetime obj else catch exception
            try:
                date_time = datetime.strptime(date_time,"%Y-%m-%dT%H:%M:%S%z")
                event_time = process_time(str(date_time.time()))
                event_date = date_time.date()

            except:
                date_time = ''
                event_time = ''
                event_date = ''
            
            library_event['Time'] = event_time
            library_event['Date'] = event_date

            # clean description string
            clean_notes = process_text(event.get('notes'))
            library_event['Desc'] = clean_notes

            yield library_event
