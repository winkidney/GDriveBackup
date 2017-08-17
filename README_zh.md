GDriveBackup
----------------

这个工具帮你用google drive来备份你的服务器.

# 特性
+ 使用 `mysqldump` 来备份MySQL数据库
+ 可以备份指定文件夹
+ 自动同步到GoogleDrive

# 安装
## 下载GoogleDrive客户端

客户端地址在： https://github.com/prasmussen/gdrive#downloads 
找到和你的系统版本匹配的客户端版本并下载

以linux-x64为例，地址为：

`https://docs.google.com/uc?id=0B3X9GlR6EmbnQ0FtZmJJUXEyRTA&export=download`

然后到你的VPS终端执行：

```
wget -O gdrive https://docs.google.com/uc?id=0B3X9GlR6EmbnQ0FtZmJJUXEyRTA&export=download
chmod a+x gdrive
sudo mv gdrive /usr/bin/
```


## 授权 Google Drive
在终端执行：

```
gdrive list
```

等待一会，终端会出现一个授权链接，在浏览器里访问授权链接，然后复制得到的授权码 `verification code`


将得到的授权码粘贴到终端的授权码粘贴处，等待完成，会出现你的google drive文件列表。


```
Id                                                  Name                              Type   Size       Created
0BwCJ3d1WooqKbU9HakpYbmRxN00                        wwwroot.tgz                       bin    35.9 MB    2017-08-15 17:38:48
0BwCJ3d1WooqKQmRLVHdwUVhaWFU                        backup                            dir               2017-08-15 13:13:44
```

`backup` 是我创建的备份用文件夹，你也可以自己创建一个文件夹来备份。
复制这个文件夹的ID，备用。

## 设置备份选项

用你喜欢的文本编辑器打开`backup.py` 并编辑如下选项：

这些选项应该根据你服务器的状况进行修改。

```
# MySQL备份选项，需要全库备份权限的账号
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "abc123"

# 备份文件夹的根
DUMP_TO = "/home/backup"    
CHILD_DUMP_DIR_NAME = "dumps"    
# 设置如上之后，你的所有备份文件都在  "/home/backup/dumps"
# 上一次的备份文件都在 "/home/backup/dumps.bak"

# 这个选项帮你把指定文件夹备份到一个tgz文件里
# 如下设置会把 '/home/kaka' 备份到 '/home/backup/dumps/wwwroot.tgz'
DIRS_TO_DUMP = [
    ("/home/kaka", "wwwroot.tgz")
]

# 这个ID是你的Google Drive 文件夹ID
# '/home/backup/dumps' 每次备份后会被同步到你的Google Drive相应文件夹
GDRIVE_DIR_ID = "dir_id"
```

## 把 `backup.py` 做成定时任务

执行:
```
ln -s `readlink -f backup.py /etc/cron.daily/backup-site`
```

然后运行 `run-parts` 命令验证cron-task是不是工作。

**注意**: 你的 `gdrvie` 认证使用的系统用户必须和cron-task执行用户一致，否则gdrive无法同步。

```
# 这条命令的执行者应该是root或者和你的cron-task执行用户一致，否则无法验证是否工作
run-parts --report -v /etc/cron.daily/
```

如果输出中看到类似 `gdrive synced`, 证明你的备份脚本已经OK了

Enjoy it.
