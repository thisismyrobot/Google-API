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

    def get_google_apps_clientlogin_headers(self):
        """ performs the authentication handshake for clientlogin
            in google apps. returns a dict of headers to add to any
            future request.
        """
        cl_post = urllib.urlencode(dict(
            accountType='HOSTED_OR_GOOGLE',
            Email=self.username,
            Passwd=self.password,
            service='writely', #docs
            source='none-none-none')
            )
        cl_url = 'https://www.google.com/accounts/ClientLogin'
        cl_data = urllib2.urlopen('https://www.google.com/accounts/ClientLogin', cl_post).read()
        cl_auth_token = cl_data.split("\n")[2].split("=")[1]
        cl_headers = {
            'Authorization':'GoogleLogin auth=%s' % cl_auth_token,
            'GData-Version':'2.0'
            }

        return cl_headers

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

        email_data_xml = libxml2.parseMemory(email_data, len(email_data))
        email_context = email_data_xml.xpathNewContext()
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

        reader_data_xml = libxml2.parseMemory(reader_data, len(reader_data))
        reader_context = reader_data_xml.xpathNewContext()
        reader_counter = reader_context.xpathEval(
            "//string[contains(text(),'com.google/reading-list')]/parent::object/number[@name='count']/text()")[0].__str__()

        return int(reader_counter)

    def get_docs(self):
        """ Returns a list of docs in you google apps account.
        """
        docs_request = urllib2.Request('https://docs.google.com/feeds/documents/private/full')
        headers = self.get_google_apps_clientlogin_headers()
        for key in headers.keys():
            docs_request.add_header(key, headers[key])

        docs_connection = urllib2.urlopen(docs_request)
        docs_data = docs_connection.read()
        docs_connection.close()

        docs_data_xml = libxml2.parseMemory(docs_data, len(docs_data))
        docs_context = docs_data_xml.xpathNewContext()
        docs_context.xpathRegisterNs('atom', 'http://www.w3.org/2005/Atom')
        docs_list = docs_context.xpathEval("//atom:feed//atom:entry/atom:title/text()")
        
        return [doc.__str__() for doc in docs_list]
