import mailbox
import email
from email.header import decode_header
import os
import pdb

if __name__ == '__main__':
    m = mailbox.mbox('./mail-inbox')
    c = 0
    dic = {}
    for message in m:
        mfrom = message.get_from()
        try:
            suffix = mfrom.split(' ')[0].split('@')[1]
        except Exception:
            # decode header first
            try:
                mfrom = decode_header(mfrom)[0][0].decode('utf-8')
                suffix = mfrom.split(' ')[0].split('@')[1]
            except Exception:
                pdb.set_trace()
        if dic.get(suffix) is None:
            dic[suffix] = []
        subject_decoded = message['subject']
        try:
            if subject_decoded is None:
                subject_decoded = 'Untitled'
        except Exception:
            pdb.set_trace()
        try:
            decoded_content = decode_header(subject_decoded)[0]
            if decoded_content[1] == 'unknown-8bit':
                try:
                    subject_decoded = decoded_content[0].decode('gb2312')
                except:
                    subject_decoded = decoded_content[0].decode('utf-8')
            elif decoded_content[1] is not None:
                subject_decoded = decoded_content[0].decode(decoded_content[1])
        except Exception:
            pdb.set_trace()
        if len(subject_decoded) == 0:
            subject_decoded = 'Untitled%d' % c
        subject_decoded = subject_decoded.replace('/','').replace(' ','_')
        dic[suffix].append(subject_decoded)
        c += 1
    # create directory and file name
    for k, v in dic.items():
        if not os.path.exists(k):
            os.mkdir(os.path.join('maildir', k))
        for name in v:
            try:
                f = open(os.path.join('maildir', k, name), 'w')
                f.close()
            except Exception:
                pdb.set_trace()
