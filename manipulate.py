#!/bin/python3
# pylint: disable=missing-module-docstring
import os
import argparse
import time
import pdb

import mailbox
from email.header import decode_header
from email.utils import parsedate

OUTPUT_DIR = 'read'
def write_dic(dic):
    tuple_obj = parsedate(dic['time'])
    year = str(tuple_obj[0])
    month = tuple_obj[1]
    day = tuple_obj[2]
    if not os.path.exists(os.path.join(OUTPUT_DIR, year)):
        os.mkdir(os.path.join(OUTPUT_DIR, year))
    str_tim = '%s-%d-%d' % (year, month, day)
    file_name = str_tim + '_' + dic['subject'] + '.md'
    content_all = dic['subject'] + '\n\n'
    content_all += dic['from'] + '\n\n'
    content_all += dic['content']
    with open(os.path.join(OUTPUT_DIR, year, file_name), 'w') as f:
        f.write(content_all)
    return

def get_decode_content(message):
    _contents = message.get_payload(decode=True)
    charset = message.get_content_charset()
    if charset is None:
        try:
            _contents = _contents.decode('utf-8')
        except:
            try:
                _contents = _contents.decode('gbk')
            except:
                pdb.set_trace()
    else:
        try:
            _contents = _contents.decode(charset)
        except:
            _contents = _contents.decode('gbk')
    return _contents

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', const=True,
        nargs='?', default=False, help='does not write to disk')

    args = parser.parse_args()
    m = mailbox.Maildir('INBOX')
    for message in m:
        dic = {}
        mfrom = message.get('from')
        decoded_content = decode_header(mfrom)[0]
        if decoded_content[1] is not None:
            mfrom = decoded_content[0].decode(decoded_content[1])
        dic['from'] = mfrom
        subject_decoded = message['subject']
        if subject_decoded is None:
            subject_decoded = 'Untitled'
        else:
            decoded_content = decode_header(subject_decoded)[0]
            if decoded_content[1] == 'unknown-8bit':
                try:
                    subject_decoded = decoded_content[0].decode('gb2312')
                except UnicodeDecodeError:
                    subject_decoded = decoded_content[0].decode('utf-8')
            elif decoded_content[1] is not None:
                subject_decoded = decoded_content[0].decode(decoded_content[1])
        if len(subject_decoded) == 0:
            subject_decoded = 'Untitled%d' % message_count
        subject_decoded = subject_decoded.replace('/', '').replace(' ', '_')
        dic['subject'] = subject_decoded
        dic['time'] = message.get('date')
        if dic['time'] is None:
            dic['time'] = message.get('Received').split(';')[-1]
        contents = ''
        if message.is_multipart():
            for part in message.walk():
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
        
