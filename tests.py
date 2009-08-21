"""
    Test for the google API - use your details and verify the results are correct
"""

import getpass
import google.api

username = raw_input("Google Account Username: ")
password = getpass.getpass("Google Account Password: ")

connector = google.api.GoogleConnector(username, password)

email_counter = connector.get_gmail_unread_count()
reader_counter = connector.get_google_reader_unread_count()

print "GMail states that you have %d unread emails" % email_counter
print "Google Reader states that you have %d unread news items" % reader_counter