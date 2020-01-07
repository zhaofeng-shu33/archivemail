## Python scripts to archive your mails from server

Steps:
1. First you need to download mails and decompress the files.
```shell
#python2
python archivemail.py --copy -v -d3600 -o $HOME/mail_archive imaps://616545598:password@imap.qq.com/INBOX
```
2. After that using `gzip -d mail-inbox.gz` to get `mail-inbox`, which is mail in MBOX format.

3. Then run `python3 manipulate.py` to generate mails in file systems.

4. Uploading to your private file storage server, for example oss:
```shell
ossutil64 cp -r maildir oss://undergraduate/maildir/
```
   Uploading to Baidu NetDisk is also a good choice.
