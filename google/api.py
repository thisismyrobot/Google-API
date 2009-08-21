import base64
import urllib
import urllib2
import libxml2


class GoogleConnector:
    """ A connector for google accounts. Provides methods to retrieve unread
        email and google reader counts. Depends on standard python 2.6 libaries
        with the exception of libxml2.
    """
    username = u''
    password = u''

    def __init__(self, username, password):
        """ Saves username + password for google account
        """
        self.username = username
        self.password = password

    def get_gmail_unread_count(self):
        """ Returns an integer representing the number of unread emails in
            a gmail inbox.
        """
        email_url = 'https://gmail.google.com/gmail/feed/atom'
        email_request = urllib2.Request(email_url)
        email_auth = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
        email_request.add_header('Authorization', 'Basic %s' % email_auth)
        email_connection = urllib2.urlopen(email_request)
        email_data = email_connection.read()
        email_connection.close()

        email_connection_xml = libxml2.parseMemory(email_data, len(email_data))
        email_context = email_connection_xml.xpathNewContext()
        email_context.xpathRegisterNs('rss', 'http://purl.org/atom/ns#')
        email_counter = email_context.xpathEval("//rss:fullcount/text()")[0].__str__()
          
        return int(email_counter)

    def get_google_reader_unread_count(self):
        """ Returns an integer representing the number of unread items in
            a google reader account.
        """
        reader_auth = urllib.urlencode(dict(Email=self.username, Passwd=self.password))
        reader_sid = urllib2.urlopen('https://www.google.com/accounts/ClientLogin', reader_auth).read().split("\n")[0]
        reader_request = urllib2.Request('http://www.google.com/reader/api/0/unread-count?all=true')
        reader_request.add_header('Cookie', reader_sid)
        reader_connection = urllib2.urlopen(reader_request)
        reader_data = reader_connection.read()
        reader_connection.close()
        
        reader_connection_xml = libxml2.parseMemory(reader_data, len(reader_data))
        reader_context = reader_connection_xml.xpathNewContext()
        reader_counter = reader_context.xpathEval(
            "//string[contains(text(),'com.google/reading-list')]/parent::object/number[@name='count']/text()")[0].__str__()

        return int(reader_counter)