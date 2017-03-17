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

def get_bug_assignments(service):
    bug_list = []
    bug_messages = service.users().messages().list(userId='me', labelIds='Label_7').execute().get('messages', [])
    for bugs in bug_messages:
        bug_message = service.users().messages().get(userId='me', id=bugs['id']).execute()
        #message_subject = service.users().messages().get(userId='me', id=bugs['id'], format='metadata', metadataHeaders='Subject').execute()
        message_subject = bug_message.get('payload', []).get('headers', [])[24]['value']
        person = re.search('\w+ (?<= )\w+', bug_message['snippet'][bug_message['snippet'].find('assigned an issue to ')+21:]).group(0)
        if person.find('Unassigned') != -1:
            #Bug is not assigned to anyone
            person = 'Unassigned'
        bug_number = re.search('\w+-\w+', message_subject[message_subject.find('Assigned: ')+10:]).group(0)
        date = bug_message['internalDate']
        new_bug = 1 # 0 - not a new bug 1 - new bug
        for bug_entry in bug_list:
            if bug_entry['internalDate'] == date:
                #message has been dealt with
                print(bug_number," repeated message")
                new_bug = 0
                break
            else:
                # new message
                if bug_entry['number'] == bug_number:
                    # bug is already in the list
                    new_bug = 0
                    if int(bug_entry['internalDate']) < int(date):
                        # current message happened after bug's last update
                        if bug_entry['assignment'] == person:
                            # bug is already assigned to this person
                            print("already assigned to person")
                            break
                        else:
                            # bug assignment changed
                            print(bug_number, " changed assignment")
                            bug_entry['assignment'] = person
                            bug_entry['internalDate'] = date
                            break
                    else:
                        #old news, doesn't matter
                        print(bug_number, " is already in list and up-to-date")
                        break
                else: 
                    # no match
                    continue
        if new_bug:
            print(bug_number," is new")
            bug_list.append({'internalDate': date, 'number': bug_number, 'assignment': person})
    return bug_list

def get_closed_bugs(service, assigned_bugs):
    bug_messages = service.users().messages().list(userId='me', labelIds='Label_11').execute().get('messages', [])
    for bugs in bug_messages:
        bug_subject = service.users().messages().get(userId='me', id=bugs['id'], format='metadata', metadataHeaders='Subject').execute().get('payload', []).get('headers', [])[0]['value']
        bug_number = re.search('\w+-\w+', bug_subject[bug_subject.find('Assigned: ')+10:]).group(0)
        try:
            assigned_bugs.remove(bug_number)
            print(bug_number)
        except Exception as error:
            print(error)
    return assigned_bugs

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    assigned_bugs = get_bug_assignments(service)
    for bug in assigned_bugs:
        print(bug)
    print(len(assigned_bugs))

if __name__ == '__main__':
    main()
