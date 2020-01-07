## Python scripts to archive your mails from server

Steps:
1. First you need to download mails and decompress the files.
```shell
python archivemail.py --copy -v -d3600 -o $HOME/mail_archive imaps://616545598:password@imap.qq.com/INBOX
```
After that using `gzip -d mail-inbox.gz` to get `mail-inbox`, which is mail in MBOX format.


Update to oss:
```shell
ossutil64 cp -r maildir oss://undergraduate/maildir/
```
