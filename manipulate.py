#!/bin/python3
import os
import argparse

import mailbox
from email.header import decode_header
from email.utils import parsedate

OUTPUT_DIR = 'read'
def write_dic(_dic):
    tuple_obj = parsedate(_dic['time'])
    year = str(tuple_obj[0])
    month = tuple_obj[1]
    day = tuple_obj[2]
    if not os.path.exists(os.path.join(OUTPUT_DIR, year)):
        os.mkdir(os.path.join(OUTPUT_DIR, year))
    str_tim = '%s-%d-%d' % (year, month, day)
    file_name = str_tim + '_' + _dic['subject'] + '.md'
    content_all = _dic['subject'] + '\n\n'
    content_all += _dic['from'] + '\n\n'
    content_all += _dic['content'].replace('&nbsp;', ' ')
    with open(os.path.join(OUTPUT_DIR, year, file_name), 'w') as f:
        f.write(content_all)

def get_decode_content(_message):
    _contents = _message.get_payload(decode=True)
    charset = _message.get_content_charset()
    if charset is None:
        try:
            _contents = _contents.decode('utf-8')
        except UnicodeDecodeError:
            _contents = _contents.decode('gbk')
    else:
        try:
            _contents = _contents.decode(charset)
        except UnicodeDecodeError:
            try:
                _contents = _contents.decode('gbk')
            except:
                _contents = _contents.decode(charset,
                    errors='ignore')
    return _contents
def decode_wrapper(content, method):
    subject_decoded = ''
    if method == 'unknown-8bit':
        try:
            subject_decoded = content.decode('gb2312')
        except UnicodeDecodeError:
            subject_decoded = content.decode('utf-8')
    elif method is not None:
            subject_decoded = content.decode(method)
    elif type(content) is str:
        subject_decoded = content
    else:
        subject_decoded = content.decode('utf-8')
    return subject_decoded

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', const=True,
                        nargs='?', default=False,
                        help='does not write to disk')
    parser.add_argument('--maildir_name', default='INBOX')
    args = parser.parse_args()
    m = mailbox.Maildir(args.maildir_name)
    for message in m:
        dic = {}
        mfrom = message.get('from')
        decoded_content = decode_header(mfrom)[0]
        if decoded_content[1] is not None:
            mfrom = decode_wrapper(decoded_content[0], decoded_content[1])
        dic['from'] = mfrom
        subject_decoded = message['subject']
        if subject_decoded is None or subject_decoded == '':
            subject_decoded = 'Untitled'
        else:
            decoded_content = decode_header(subject_decoded)[0]
            subject_decoded = decode_wrapper(decoded_content[0], decoded_content[1])
        subject_decoded = subject_decoded.replace('/', '').replace(' ', '_')
        dic['subject'] = subject_decoded
        dic['time'] = message.get('date')
        if dic['time'] is None:
            if message.get('Received') is not None:
                dic['time'] = message.get('Received').split(';')[-1]
            else:
                # mail from 10000@qq.com
                continue
        contents = ''
        if message.is_multipart():
            for part in message.walk():
                if type(part) is mailbox.MaildirMessage:
                    continue
                if part.is_multipart():
                    for subpart in part.walk():
                        if subpart.get_content_type() == 'text/plain':
                            contents += get_decode_content(subpart) + '\n'
                elif part.get_content_type() == 'text/plain':
                    contents += get_decode_content(part) + '\n'
        elif message.get_content_type() == 'text/plain':
            contents += get_decode_content(message) + '\n'
        dic['content'] = contents
        if not args.dry_run:
            write_dic(dic)
