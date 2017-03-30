import base64
import email
from apiclient import errors

def GetMimeMessage(service, user_id, msg_id):
    try:
            message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
            print('Message snippet: '+message['snippet'])
            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
            mime_msg = email.message_from_string(msg_str)
            return mime_msg
    except Exception as error:
            print('An error occurred: ',error)

def get_mpart(mail):
    maintype = mail.get_content_maintype()
    if maintype == 'multipart':
        for part in mail.get_payload():
            # This includes mail body AND text file attachments.
            if part.get_content_maintype() == 'text':
                return part.get_payload()
        # No text at all. This is also happens
        return ""
    elif maintype == 'text':
        return mail.get_payload()


def get_mail_body(mail):
    """
    There is no 'body' tag in mail, so separate function.
    :param mail: Message object
    :return: Body content
    """
    body = ""
    if mail.is_multipart():
        # This does not work.
        # for part in mail.get_payload():
        #    body += part.get_payload()
        body = get_mpart(mail)
    else:
        body = mail.get_payload()
    return body
