import base64
import urllib
import urllib2
import xml.dom.minidom


class GoogleConnector:
    """ a connector for google accounts. provides methods to retrieve unread
        email and google reader counts
    """
    username = u''
    password = u''

    def __init__(self, username, password):
        """ constructor - takes username + password for google account
        """
        self.username = username
        self.password = password

    def get_gmail_unread_count(self):
        """ returns an integer representing the number of unread emails in
            a gmail inbox.
        """
        email_url = 'https://gmail.google.com/gmail/feed/atom'
        email_request = urllib2.Request(email_url)
        email_auth = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
        email_request.add_header("Authorization", "Basic %s" % email_auth)
        email_connection = urllib2.urlopen(email_request)
        email_data = email_connection.read();
        email_connection.close()
        email_dom = xml.dom.minidom.parseString(email_data)
        email_counter = int(email_dom.getElementsByTagName('fullcount')[0].childNodes[0].data)
        return email_counter

    def get_google_reader_unread_count(self):
        """ returns an integer representing the number of unread items in
            a google reader account.
        """
        reader_auth = urllib.urlencode(dict(Email=self.username, Passwd=self.password))
        reader_sid = urllib2.urlopen('https://www.google.com/accounts/ClientLogin', reader_auth).read().split("\n")[0]
        reader_request = urllib2.Request('http://www.google.com/reader/api/0/unread-count?all=true')
        reader_request.add_header('Cookie', reader_sid)
        reader_connection = urllib2.urlopen(reader_request)
        reader_data = reader_connection.read()
        reader_connection.close()
        reader_dom = xml.dom.minidom.parseString(reader_data)
        reader_counter = 0
        for reader_dom_object in reader_dom.getElementsByTagName('object'):
            if reader_dom_object.getElementsByTagName('string'):
                if str(reader_dom_object.getElementsByTagName('string')[0].childNodes[0].data).endswith('google/reading-list'):
                    reader_counter = int(reader_dom_object.getElementsByTagName('number')[0].childNodes[0].data)
        return reader_counter