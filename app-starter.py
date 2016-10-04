#!/usr/bin/python

import os

import subprocess

import sys

import time

import datetime

usr_home = os.path.expanduser('~')
cwd = os.getcwd()
# project = os.path.abspath("~/workspace/coding/user")
project = os.path.expanduser("~/workspace/coding/user/user-biz")
app = os.path.basename(project)

targetDir = os.path.join(project, "target")


def findTarget(target):
    for x in os.listdir(target):
        if x.endswith(".jar"):
            return x


def findPid(app):
    # ignore the grep command itself
    return execShell("ps aux | grep %s | grep jar | grep -v grep | awk '{print $2}'" % app)


def kill(pid):
    return shell("kill -9 %s" % pid)


def execShell(cmd):
    l = shell(cmd)
    return l[0]


def shell(cmd):
    return os.popen(cmd).readlines()


def startApp(jar):
    ps = subprocess.Popen(" java -jar %s &" % os.path.join(targetDir, jar), stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          shell=True)
    startTime = datetime.datetime.now()
    while True:
        data = ps.stdout.readline()
        print "-----------", data, data.find("server started")
        if data.find("server started") > 0:
            if ps.poll() is not None:
                print app, " server started !!!!!"
                return
        else:
            cur = datetime.datetime.now()
            if (cur - startTime).seconds > 10:
                raise Exception("time out waiting for the server to start .. ")


def init():
    global app
    global targetDir
    app = os.path.basename(project)
    validDir(project)
    targetDir = os.path.join(project, "target")
    validDir(targetDir)


def validDir(dir, msg=None):
    if not os.path.isdir(dir):
        if not msg:
            raise Exception("invalid dir : %s" % dir)
        raise Exception("%s :%s " % (dir, msg))


def start():
    jar = findTarget(targetDir)
    if not jar:
        raise Exception("no runnable jar found")
    pid = findPid(app)
    if pid:
        kill(pid)
        print "killed", pid
    startApp(jar)
    print "new pid ", findPid(app)


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print "app-starter.py [projectDir]"
        exit(0)
    project = os.path.expanduser(args[1])
    print "project dir : ", project
    init()
    print os.getcwd()
    print project
    print shell("ls ")
    print targetDir
    print "got", findTarget(targetDir)
    print os.path.basename(project)
    print findPid(app)
    print "=============================="
    start()
