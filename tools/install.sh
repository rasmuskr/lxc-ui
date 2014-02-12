


if [[ "$UID" -ne "0" ]];then
	echo 'You must be root to run the installer!'
	exit
fi


INSTALL_DIR='/srv/lxc-ui'

######################## Installing dependencies
echo 'Installing dependencies'
apt-get update &> /dev/null

hash python &> /dev/null || {
	echo '+ Installing Python'
	apt-get install -y python > /dev/null
}

hash pip &> /dev/null || {
	echo '+ Installing Python pip'
	apt-get install -y python-pip > /dev/null
}

hash virtualenv &> /dev/null || {
	echo '+ Installing virtualenv'
	apt-get install -y python-virtualenv > /dev/null
}

########################### Install git and clone
hash git &> /dev/null || {
	echo '+ Installing Git'
	apt-get install -y git > /dev/null
}

git clone https://github.com/rasmuskr/lxc-ui.git "$INSTALL_DIR"



########################## Making virtual env

virtualenv "$INSTALL_DIR/lxc-ui-virtualenv"

"$INSTALL_DIR/lxc-ui-virtualenv/bin/pip" install -r "$INSTALL_DIR/lxc-ui-agent/requirements.txt"


########################## Installing auto start script
echo 'Adding /etc/init.d/lxc-ui-agent...'

cat > '/etc/init.d/lxc-ui-agent' <<EOF
#!/bin/bash
#
# /etc/init.d/lxc-ui-agent
#
### BEGIN INIT INFO
# Provides: lxc-ui-agent
# Required-Start: \$local_fs \$network
# Required-Stop: \$local_fs
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: lxc-ui-agent Start script
### END INIT INFO


WORK_DIR="$INSTALL_DIR"
SCRIPT="lxc-ui-agent.py"
DAEMON="\$WORK_DIR/lxc-ui-virtualenv/bin/python \$WORK_DIR/lxc-ui-agent/\$SCRIPT"
PIDFILE="/var/run/lxc-ui-agent.pid"
USER="root"

function start () {
	echo -n 'Starting server...'
	/sbin/start-stop-daemon --start --pidfile \$PIDFILE \\
		--user \$USER --group \$USER \\
		-b --make-pidfile \\
		--chuid \$USER \\
		--chdir \$WORK_DIR \\
		--exec \$DAEMON
	echo 'done.'
	}

function stop () {
	echo -n 'Stopping server...'
	/sbin/start-stop-daemon --stop --pidfile \$PIDFILE --signal KILL --verbose
	echo 'done.'
}


case "\$1" in
	'start')
		start
		;;
	'stop')
		stop
		;;
	'restart')
		stop
		start
		;;
	*)
		echo 'Usage: /etc/init.d/lxc-ui-agent {start|stop|restart}'
		exit 0
		;;
esac

exit 0
EOF


chmod +x '/etc/init.d/lxc-ui-agent'
update-rc.d lxc-ui-agent defaults &> /dev/null


/etc/init.d/lxc-ui-agent start





