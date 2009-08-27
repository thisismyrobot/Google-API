"""
    Test for the google API - use your details and verify the results are correct
"""

import getpass
import google.api

username = raw_input("Google Account Email Address: ")
password = getpass.getpass("Google Account Password: ")

connector = google.api.GoogleConnector(username, password)

email_counter = connector.get_gmail_unread_count()
reader_counter = connector.get_google_reader_unread_count()
documents = connector.get_docs()

print "GMail states that you have %d unread emails" % email_counter
print "Google Reader states that you have %d unread news items" % reader_counter
print "These are your google documents:"
for document in documents:
    print " * %s" % document

