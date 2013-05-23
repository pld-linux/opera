#!/bin/sh
# set JAVA_HOME from jpackage-utils if available
if [ -f /usr/share/java-utils/java-functions ]; then
	. /usr/share/java-utils/java-functions
	set_jvm
fi
export OPERA_DIR=/usr/share/opera
export OPERA_PERSONALDIR=$HOME/.opera
exec /usr/lib/opera/opera "$@"
