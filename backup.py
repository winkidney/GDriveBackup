#!/usr/bin/env python

# config
import os
import subprocess

# config

MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "abc123"
DUMP_TO = "/home/backup"
CHILD_DUMP_DIR_NAME = "dumps"

DIRS_TO_DUMP = [
    ("/home/kaka", "wwwroot.tgz")
]


GDRIVE_DIR_ID = "dir_id"

# constants
FULL_DUMP_DIR = os.path.join(DUMP_TO, CHILD_DUMP_DIR_NAME)
FULL_DUMP_DIR_BAK = os.path.join(DUMP_TO, CHILD_DUMP_DIR_NAME + ".bak")

GDRVIE_MAP = [
    (FULL_DUMP_DIR, GDRIVE_DIR_ID),
]

MYSQL_DUMP_CMD_TPL = "mysqldump" \
                     " --defaults-extra-file={dump_config_path}" \
                     " --all-databases" \
                     " > {out_file}"

MYSQL_CONFIG_TPL = """
[mysqldump]
user={username}
password={password}

"""


def exec_cmd(command, ignore_error=False):
    stream = subprocess.Popen(
        command,
        shell=True,
    )
    stream.communicate()
    if stream.returncode != 0:
        if not ignore_error:
            raise ValueError("Failed to execute command: %s" % command)


def _ensure_path():
    if not os.path.exists(DUMP_TO):
        exec_cmd(
            "mkdir -p %s" % DUMP_TO
        )


def _mk_bak():
    if os.path.exists(FULL_DUMP_DIR):
        if os.path.exists(FULL_DUMP_DIR_BAK):
            exec_cmd(
                "rm -fr %s" % FULL_DUMP_DIR_BAK
            )
        exec_cmd(
            "mv -f %s %s" % (FULL_DUMP_DIR, FULL_DUMP_DIR_BAK)
        )
    exec_cmd(
        "mkdir -p %s" % FULL_DUMP_DIR
    )


class MySQLDump(object):
    _config_path = "/tmp/.sqlpwd"
    _db_file_name = "all_database.bak.sql"

    @property
    def out_file(self):
        return os.path.join(
            FULL_DUMP_DIR,
            self._db_file_name,
        )

    def _mk_config(self):
        content = MYSQL_CONFIG_TPL.format(
            username=MYSQL_USERNAME,
            password=MYSQL_PASSWORD,
        )
        with open(self._config_path, "w") as f:
            f.write(content)

    def _dump_db(self):
        cmd = MYSQL_DUMP_CMD_TPL.format(
            dump_config_path=self._config_path,
            out_file=self.out_file,
        )
        exec_cmd(cmd)

    def _clean(self):
        exec_cmd("rm -f %s" % self._config_path)

    def run(self):
        self._mk_config()
        self._dump_db()
        self._clean()


class DIRDump(object):
    def __init__(self, dirs_to_dump):
        self._dirs = dirs_to_dump

    def _tar_czf(self):
        for folder, archive_name in self._dirs:
            out_file = os.path.join(FULL_DUMP_DIR, archive_name)
            exec_cmd(
                "tar czf %s %s" % (out_file, folder)
            )
            print("folder %s dumped to %s" % (folder, out_file))

    def run(self):
        self._tar_czf()


def sync_gdrive(paths):
    for path, remote_path_id in paths:
        exec_cmd(
            "gdrive sync upload {path} {remote_path_id}".format(
                path=path,
                remote_path_id=remote_path_id,
            )
        )


def main():
    _ensure_path()
    _mk_bak()
    print("Old files deleted, last recent backup moved to old directory.")
    sql = MySQLDump()
    sql.run()
    print("Mysql dumped to %s" % sql.out_file)
    print("File state: %s" % os.stat(sql.out_file))
    d = DIRDump(DIRS_TO_DUMP)
    d.run()
    print("Directories dumped.")
    sync_gdrive(GDRVIE_MAP)
    print("Google Drive synced.")


if __name__ == "__main__":
    main()
