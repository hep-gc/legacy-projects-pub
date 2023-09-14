#!/bin/sh
#
# chkconfig:    345 85 15
# description:  nep52 accoutant data collector process
#
### BEGIN INIT INFO
# Provides:          nep52accountant-collector
# Required-Start:    $syslog $remote_fs $network
# Should-Start:      
# Required-Stop:     $syslog $remote_fs $network
# Should-Stop:       
# Default-Start:     3 5
# Default-Stop:      0 1 2 6
# Short-Description: nep52 accoutant data collector process
# Description:       
### END INIT INFO

EXECUTABLEPATH="/usr/local/nep52accountant/bin/nep52accountant-collector" 

# Non-default python (eg. if you installed python 2.6 on RHEL5)
PYTHON=""

# You probably won't want to change these.
SERVICE=nep52accountant-collector
CRASHLOG=/tmp/${SERVICE}.crash.log
PIDSPATH=/var/run
PIDFILE=$PIDSPATH/$SERVICE.pid

test -x $EXECUTABLEPATH || { echo "$EXECUTABLEPATH not installed"; 
	if [ "$1" = "stop" ]; then exit 0;
	else exit 5; fi; }

ok () {
    echo -e "\t\t\t\t[ " "\e[0;32mOK\e[0m" " ]"
}

start () {
    if [ -f $PIDFILE ]; then
        PID=`cat $PIDFILE`
        ps $PID >/dev/null
        IS_NOT_RUNNING=$?
        if [ $IS_NOT_RUNNING ]; then
            echo $"$SERVICE didn't shut down cleanly last time."
            rm -f $PIDFILE
        else
            PID=`cat $PIDFILE`
            echo $"$SERVICE is already running with PID ${PID}."
            return 1
        fi
    fi

    echo -n $"Starting $SERVICE:"
    if [ "$SUDO_COMMAND" ]; then
        sudo nohup ${PYTHON} ${EXECUTABLEPATH} </dev/null >${CRASHLOG} 2>&1 &
        echo $! > $PIDFILE
    else
        nohup ${PYTHON} ${EXECUTABLEPATH} </dev/null >${CRASHLOG} 2>&1 &
        echo $! > $PIDFILE
    fi
    RETVAL=$?
    touch /var/lock/subsys/$SERVICE
    ok
}

stop () {
    if [ -f $PIDFILE ]; then
        echo -n $"Stopping $SERVICE:"
	PID=`cat $PIDFILE`
        /bin/kill $PID
	while ps -p $PID >/dev/null; do sleep 1; done
        if [ $? -eq 0 ]; then
            rm -f $PIDFILE >/dev/null 2>&1
        fi
        rm -f /var/lock/subsys/$SERVICE
    	ok
    fi
}


RETVAL=0

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
	if [ -f $PIDFILE ]; then
        PID=`cat $PIDFILE`
        ps $PID >/dev/null
        IS_RUNNING=$?
        if [ $IS_RUNNING ]; then
            PID=`cat $PIDFILE`
            echo $"$SERVICE is running with PID ${PID}."
        else
            echo $"$SERVICE has exited unexpectedly."
        fi
	else
		echo "$SERVICE isn't running."
	fi
        ;;
    restart)
        stop
        start
        ;;
    *)
        echo $"Usage: $0 {start|stop|restart|status|}"
        exit 3
        ;;
esac

exit $RETVAL
