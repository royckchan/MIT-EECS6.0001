# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        '''
        Initialize a NewsStory object
        
        guid: string, globally unique identifier
        title: string
        description: string
        link: string, link to more content
        pubdate: datetime, date the news was published
        '''
        
        self.guid = guid
        self.title = title
        self.description =  description
        self.link = link
        self.pubdate = pubdate
    
    '''
    The following getter methods are used to safely access data attributes outside of the class
    '''
    
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        '''
        Initialize a PhraseTrigger object, by lowercasing and adding spaces at the front and at the end respectively
        phrase: string
        '''
        self.phrase = ' ' + phrase.lower() + ' '
    
    def is_phrase_in(self, text):
        # Lowercase the input text
        processing_text = text.lower()
        
        # Replace punctuation by space
        for punctuation in string.punctuation:
            processing_text = processing_text.replace(punctuation, ' ')
        
        # Make sure there is a single space between the words (and at the frond and at the end)
        processing_text = ' ' + ' '.join(processing_text.split()) + ' '
        return self.phrase in processing_text

# Problem 3
# TODO: TitleTrigger

class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
# TODO: DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, time):
        self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        self.time.replace(tzinfo=pytz.timezone("EST"))

# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        return (self.time > story.get_pubdate())

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        return (self.time < story.get_pubdate())

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(object):
    def __init__(self, Trigger):
        self.trigger = Trigger
    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# Problem 8
# TODO: AndTrigger

class AndTrigger(object):
    def __init__(self, Trigger1, Trigger2):
        self.trigger1 = Trigger1
        self.trigger2 = Trigger2
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)

# Problem 9
# TODO: OrTrigger

class OrTrigger(object):
    def __init__(self, Trigger1, Trigger2):
        self.trigger1 = Trigger1
        self.trigger2 = Trigger2
    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
#    return stories

    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
                break
    return filtered_stories


#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!
    
    all_triggers = {}
    trigger_list = []
    
    for line in lines[1:]:
        line_split = line.split(',')
        if line_split[0] == 'ADD':
            for trigger_name in line_split[1:]:
                trigger_list.append(all_triggers[trigger_name])
        elif len(line_split) == 3:
            trigger_name, trigger_type, trigger_criteria = line_split
            if trigger_type == 'TITLE':
                all_triggers[trigger_name] = TitleTrigger(trigger_criteria)
            elif trigger_type == 'DESCRIPTION':
                all_triggers[trigger_name] = DescriptionTrigger(trigger_criteria)
            elif trigger_type == 'AFTER':
                all_triggers[trigger_name] = AfterTrigger(trigger_criteria)
            elif trigger_type == 'BEFORE':
                all_triggers[trigger_name] = BeforeTrigger(trigger_criteria)
            elif trigger_type == 'NOT':
                all_triggers[trigger_name] = NotTrigger(all_triggers[trigger_criteria])
        elif len(line_split) == 4:
            trigger_name, composite_type, trigger_name_1, trigger_name_2 = line_split
            if composite_type == 'AND':
                all_triggers[trigger_name] = AndTrigger(all_triggers[trigger_name_1], all_triggers[trigger_name_2])
            elif composite_type == 'OR':
                all_triggers[trigger_name] = OrTrigger(all_triggers[trigger_name_1], all_triggers[trigger_name_2])
    return trigger_list

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line
        
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

# Remarks:
# 1. The US Presidential Election 2016 is too outdated to get any news feed, but the above code
# works fine if you edit the "triggers.txt" file to fire on current news stories.
# 2. I think there are some bugs with TimeTrigger (i.e., BeforeTrigger and AfterTrigger), although
# they pass the test cases. However, I don't know how to fix them yet.