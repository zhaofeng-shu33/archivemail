#!/bin/python3
import os
import argparse
import re
import mailbox
from email.header import decode_header
from email.utils import parsedate

OUTPUT_DIR = 'read'
p = re.compile('[\\/:?*?<>|]+')
def get_time_str(email_time):
    tuple_obj = parsedate(email_time)
    year = str(tuple_obj[0])
    month = tuple_obj[1]
    day = tuple_obj[2]    
    str_time = '%s-%d-%d' % (year, month, day)
    return (str_time, year)
 
def write_dic(_dic):
    str_tim, year = get_time_str(_dic['time'])
    if not os.path.exists(os.path.join(OUTPUT_DIR, year)):
        os.mkdir(os.path.join(OUTPUT_DIR, year))
    file_name = str_tim + '_' + _dic['subject'] + '.md'
    file_name = re.sub(p, '_', file_name)
    content_all = _dic['subject'] + '\n\n'
    content_all += _dic['from'] + '\n\n'
    content_all += _dic['to'] + '\n\n'
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

def add_content(mess, _set):
    _len = len(_set)
    _set.add(mess)
    if len(_set) == _len:
        return ''
    return mess + '\n'

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
        mto = message.get('to')
        if type(mto) is str:
            dic['to'] = mto
        elif mto is None:
            dic['to'] = ''
        else:
            decoded_content = decode_header(mto)[-1]
            dic['to'] = decode_wrapper(decoded_content[0], decoded_content[1])
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
        _set = set()
        #str_time, _ = get_time_str(dic['time'])
        #if str_time == '2022-3-7':
        #    import pdb
        #    pdb.set_trace()
        if message.is_multipart():
            for part in message.walk():
                if type(part) is mailbox.MaildirMessage:
                    continue
                if part.is_multipart():
                    for subpart in part.walk():
                        if subpart.get_content_type() == 'text/plain':
                            contents += add_content(get_decode_content(subpart), _set) 
                elif part.get_content_type() == 'text/plain':
                    contents += add_content(get_decode_content(part), _set)
        elif message.get_content_type() == 'text/plain':
            contents += add_content(get_decode_content(message), _set)
        dic['content'] = contents
        if not args.dry_run:
            write_dic(dic)
