## Python scripts to archive your mails from server

Steps:
1. First you need to download mails using `offlineimap` with python2 interpreter.

```shell
../offlineimap/bin/offlineimap -f "Sent Items"
```

2. Then run `python3 manipulate.py` to generate readable mails in file systems. The `manipulate.py` only extracts plain text mail content from `INBOX`.

For specific directory, use
```shell
python3 manipulate.py --maildir_name Sent
```

3. Uploading to your private file storage server, for example oss:
```shell
ossutil64 cp -rf read oss://undergraduate/maildir/
```
   Uploading to Baidu NetDisk is also a good choice.
## Other uploading option
```shell
# compress first
tar -czvf read.tar.gz read/
```
You can also use `mutt` console client program to
read the archived mail. That is `mail -f /home/feng/imap-maildir/INBOX/`
