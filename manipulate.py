#!/bin/python3
# pylint: disable=missing-module-docstring
import os
import argparse

import mailbox
from email.header import decode_header

def write_to_disk(dic_obj):
    '''write archive results
    '''
    # create directory and file name
    if not os.path.exists('maildir'):
        os.mkdir('maildir')
    for key, value in dic_obj.items():
        if not os.path.exists(key):
            os.mkdir(os.path.join('maildir', key))
        for name in value:
            file_obj = open(os.path.join('maildir', key, name), 'w')
            file_obj.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', const=True,
                        nargs='?', default=False, help='does not write to disk')
    args = parser.parse_args()
    mailbox_instance = mailbox.mbox('./mail-inbox')
    message_count = 0
    dic = {}
    for message in mailbox_instance:
        mfrom = message.get_from()
        decoded_content = decode_header(mfrom)[0]
        if decoded_content[1] is not None:
            mfrom = decoded_content[0].decode(decoded_content[1])
        suffix = mfrom.split(' ')[0].split('@')[1]
        if dic.get(suffix) is None:
            dic[suffix] = []
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
        dic[suffix].append(subject_decoded)
        message_count += 1

    if not args.dry_run:
        write_to_disk(dic)
