#!/bin/sh

migrate_profiledir() {
	# restore location of opera dir for new opera to do automatic profile migration
	# we used to setup OPERA_PERSONALDIR to use XDG config path
	# but seems there's no way to tell new opera where to take old profile for
	# migration than it's hardcoded $HOME/.opera
	# so we move stuff back there before launching opera

	DOT_DIR="$HOME/.opera"
	XDG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/opera"

	# skip if already migrated
	if [ -e $XDG_DIR/Preferences ]; then
		return
	fi

	OPERA_PERSONALDIR=$DOT_DIR
	if [ ! -d "$OPERA_PERSONALDIR/operaprefs.ini" ]; then
		OPERA_PERSONALDIR=$XDG_DIR
	fi

	if [ "$OPERA_PERSONALDIR" = "$DOT_DIR" ]; then
		# already there
		return
	fi

	# if ~/.opera contains just OperaAutoupdateChecker.sqlite, remove it
	rm -f $DOT_DIR/OperaAutoupdateChecker.sqlite
	test -d "$DOT_DIR" && rmdir --ignore-fail-on-non-empty $DOT_DIR

	# neither dir exists, nothing to do
	if [ ! -d "$DOT_DIR" ] && [ ! -d $XDG_DIR ]; then
		return
	fi

	# if no dir, just move
	if [ ! -d "$DOT_DIR" ]; then
		mv $XDG_DIR $DOT_DIR
		return
	fi

	# may attempt to figure which dir is newer and then rename
}

migrate_profiledir

exec /usr/lib/opera/opera "$@"
