#!/bin/sh
# set JAVA_HOME from jpackage-utils if available
if [ -f /usr/share/java-utils/java-functions ]; then
	. /usr/share/java-utils/java-functions
	set_jvm
fi
export OPERA_DIR=/usr/share/opera

# Legacy dir
export OPERA_PERSONALDIR="$HOME/.opera"

# XDG path
if [ ! -d "$OPERA_PERSONALDIR/operaprefs.ini" ]; then
	OPERA_PERSONALDIR="${XDG_CONFIG_HOME:-$HOME/.config}/opera"
fi

exec /usr/lib/opera/opera "$@"
