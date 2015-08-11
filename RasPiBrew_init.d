#! /bin/sh
### BEGIN INIT INFO
# Provides:          RasPiBrew
# Required-Start:    $local_fs 
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: RasPiBrew
# Description: Raspberry Pi Brewhouse Controller
### END INIT INFO

DIR=/usr/share/adafruit/webide/repositories/rpibrewcontrol/rpiBrewControl
DAEMON=$DIR/run.sh
DAEMON_NAME=RasPiBrew

DAEMON_OPTS=""
DAEMON_USER=root

PIDFILE=/var/run/$DAEMON_NAME.pid

. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "Starting system $DAEMON_NAME daemon"
    cd $DIR
    start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER --chdir $DIR --startas $DAEMON -- $DAEMON_OPTS
    log_end_msg $?
}

do_stop () {
    log_daemon_msg "Stopping system $DAEMON_NAME daemon"
    start-stop-daemon --stop --pidfile $PIDFILE --retry 10
    log_end_msg $?
}


case "$1" in
  start|stop)
    do_${1}
    ;;

  restart|reload|force-relaod)
    do_stop
    do_start
    ;;

 status)
    status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
    ;;

 *)
    echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}"
    exit 1
    ;;

esac
exit 0
