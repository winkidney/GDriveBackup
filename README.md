GDriveBackup
----------------

[中文README](README_zh.md)

This tool helps you backup your server with google drive

# Feature
+ MySQL backup by `mysqldump`
+ Backup for specified folders
+ Sync backup folder to google drive

# Install

## Download

Go to https://github.com/prasmussen/gdrive#downloads and find a link for your
OS version (for example linux.x86-64)

The link is: 

`https://docs.google.com/uc?id=0B3X9GlR6EmbnQ0FtZmJJUXEyRTA&export=download`

Then go to your vps and execute following commands:

```
wget -O gdrive https://docs.google.com/uc?id=0B3X9GlR6EmbnQ0FtZmJJUXEyRTA&export=download
chmod a+x gdrive
sudo mv gdrive /usr/bin/
```


## Authorize Google Drive
Run:

```
gdrive list
```

You will get a link, then open the link in your browser and get a `verification code`.
Copy the code and paste it back to the vps's commandline.

Then, wait for `gdrive` to finish its work.
 

Then you will see a list like:

```
Id                                                  Name                              Type   Size       Created
0BwCJ3d1WooqKbU9HakpYbmRxN00                        wwwroot.tgz                       bin    35.9 MB    2017-08-15 17:38:48
0BwCJ3d1WooqKQmRLVHdwUVhaWFU                        backup                            dir               2017-08-15 13:13:44
```

The `backup` folder is my folder for backup-worker to sync, you could create your own folder.

Now we assume that you use `backup` as the default backup folder.

Copy the `Id` of the folder you choose: `0BwCJ3d1WooqKQmRLVHdwUVhaWFU`.

# Setup Backup

## Set backup options 

Edit `backup.py` with your favorite text editor.

Following options should be changed to your own value.

```
# Mysql dump options, all database will be dumped to single file.
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "abc123"

DUMP_TO = "/home/backup"    # backup's root folder
CHILD_DUMP_DIR_NAME = "dumps"    
# Your current backup will be  "/home/backup/dumps"
# Last recent backup will be "/home/backup/dumps.bak"

# This option will backup given folder to specified tgz file
# For example, this settings will backup '/home/kaka' to '/home/backup/dumps/wwwroot.tgz'
DIRS_TO_DUMP = [
    ("/home/kaka", "wwwroot.tgz")
]

# This is your gdrive folder id
# '/home/backup/dumps' will be synced with this folder each time
GDRIVE_DIR_ID = "dir_id"
```

## Link backup.py as cron-task

I use:
```
ln -s `readlink -f backup.py /etc/cron.daily/backup-site`
```

The run `run-parts` command to see if the cron will run correctly.

**Note**: Your `gdrvie` authorization should be set with the same user as 
you run the cron task.

```
# Should be run as root or the user you run the cron task. 
run-parts --report -v /etc/cron.daily/
```

Now if the command output something like `gdrive synced`, your backup works well.

Enjoy it.
