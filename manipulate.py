#!/bin/python3
import os
import argparse

import mailbox
import email
from email.header import decode_header

OUTPUT_DIR = 'read'
def write_dic(dic):
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', const=True,
        nargs='?', default=False, help='does not write to disk')
    args = parser.parse_args()
    m = mailbox.Maildir('INBOX')
    message_count = 0
    for message in m:
        dic = {}
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
                except:
                    subject_decoded = decoded_content[0].decode('utf-8')
            elif decoded_content[1] is not None:
                subject_decoded = decoded_content[0].decode(decoded_content[1])
        if len(subject_decoded) == 0:
            subject_decoded = 'Untitled%d' % message_count
        subject_decoded = subject_decoded.replace('/', '').replace(' ', '_')
        dic[suffix].append(subject_decoded)
        message_count += 1

        if not args.dry_run:
            write_dic(dic)
