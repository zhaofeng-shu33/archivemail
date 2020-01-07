```shell
python archivemail.py --copy -v -d3600 -o $HOME/mail_archive imaps://616545598:password@imap.qq.com/INBOX
```

Update to oss:
```shell
ossutil64 cp -r maildir oss://undergraduate/maildir/
```