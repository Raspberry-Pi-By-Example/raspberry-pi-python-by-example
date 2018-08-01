import os
import sys

PIDFILE = "/var/run/my-daemon.pid"
LOGFILE = "/var/log/my-daemon.log"

def daemonize(pidfile, logfile):
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)

    except OSError, e:
        print("Fork #1 failed: {} ({})".format(e.errno, e.strerror))
        sys.exit(1)

    os.chdir("/")
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            fpid = open(pidfile, 'w')
            fpid.write(str(pid))
            fpid.close()
            sys.exit(0)
    except OSError, e:
        print("Fork #2 failed: {} ({})".format(e.errno, e.strerror))
        sys.exit(1)

    si = file("/dev/null", 'r')
    so = file(logfile, 'a+')
    se = file("/dev/null", 'a+', 0)

    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

