from __future__ import print_function
import httplib2
import os
import re

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Test Bug Assignment Parser'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python-bug-parser.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to '+ credential_path)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    bug_messages = service.users().messages().list(userId='me', labelIds='Label_7').execute().get('messages', [])
    for bugs in bug_messages:
        bug_message = service.users().messages().get(userId='me', id=bugs['id'], format='metadata', metadataHeaders='snippet').execute()
        assigned_to = bug_message['snippet'][bug_message['snippet'].find('assigned an issue to ')+21:]
        person = re.search('\w+ (?<= )\w+ ', assigned_to).group(0)
        if person == 'Tyler Gilbert ':
            message_subject =  service.users().messages().get(userId='me', id=bugs['id'], format='metadata', metadataHeaders='Subject').execute().get('payload', []).get('headers', [])[0]['value']
            bug_number = re.search('\w+-\w+', message_subject[message_subject.find('Assigned: ')+10:]).group(0)
            print(person," - ",bug_number)

if __name__ == '__main__':
    main()
