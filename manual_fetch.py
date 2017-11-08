#Created By: Milad Khoshdel
#Blog: https://blog.regux.com
#Email: miladkhoshdel@gmail.com
#Telegram: @miladkho5hdel


from ftplib import FTP
from datetime import datetime
import sqlite3
import os
import argparse
import sys


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None


def ftp_connect(ip, user, password, file, cwddir):
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    try:
        ftp = FTP(str(ip))
        ftp.login(str(user), str(password))
        ftp.cwd("/" + str(cwddir))
        files = ftp.nlst()
        if not os.path.exists(dir_path + "\\download\\" + ip):
            os.makedirs(dir_path + "\\download\\" + ip)

        print("  - Downloading " + file + " from " + ip)
        ftp.retrbinary("RETR " + file,
                       open(dir_path + "\\download\\" + ip + "\\" + file, 'wb').write)
        print("  - Downloading Done.")
        ftp.close()
    except Exception as e:
        print("  - Error: " + str(e))
        pass


def insertdb(ip, filename):
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    try:
        with open(dir_path + "\\download\\" + ip + "\\" + filename) as f:
            content = f.readlines()
        print("  - Reading File ...")
        items = []
        for i in content:
            b = i.strip().split(":")
            print("   - " + b[0] + ": " + b[1])
            items.append(b[1])
        print("  - Reading File Done...")
        items.append(ip)
        database = dir_path + r"\newdb.sqlite"
        conn = create_connection(database)
        cur = conn.cursor()
        print("  - inserting data in DB ...")
        cur.execute("SELECT * FROM informations WHERE ipaddress = ?", (ip,))
        data = cur.fetchall()
        if len(data) == 0:
            cur.execute(
                "INSERT INTO 'informations' ('webserver','databaseserver','ftpserver','ipaddress') VALUES (?,?,?,?)",
                items)
            conn.commit()
        else:
            cur.execute(
                '''UPDATE informations SET webserver = ?, databaseserver = ?, ftpserver = ? WHERE ipaddress = ?''',
                items)
            conn.commit()
        print("  - inserting data in DB Done.")
    except Exception as e:
        print(e)
        pass

def banner():
    print(' ')
    print('  Usage: ./manual_fetch.py [options]')
    print(' ')
    print('  Options: -s, --server    <hostname/ip>   |   Host')
    print('           -u, --user      <user>          |   User')
    print('           -p, --password  <password>      |   Password')
    print('           -c, --cwd       <directory>     |   FTP Path')
    print('           -f, --filename  <filename>      |   File Name')
    print(' ')
    print('  Example: ./manual_fetch.py -s 192.168.1.1 -u root -p 123123 -c download/files -f list.txt')


def main():
    start = datetime.now()
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path + "\\download"):
        os.makedirs(dir_path + "\\download")
    database = dir_path + r"\newdb.sqlite"
    conn = create_connection(database)

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server")
    parser.add_argument("-u", "--user")
    parser.add_argument("-p", "--password")
    parser.add_argument("-c", "--cwd")
    parser.add_argument("-f", "--filename")
    args = parser.parse_args()

    if not args.server or not args.user or not args.password or not args.filename:
        banner()
        sys.exit(0)

    ipaddr = args.server
    username = args.user
    password = args.password
    pathcwd = args.cwd
    filename = args.filename

    print("+ Connectiong to " + ipaddr)
    ftp_connect(ipaddr, username, password, filename, pathcwd)
    insertdb(ipaddr, filename)

if __name__ == '__main__':
    main()
