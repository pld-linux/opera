#!/bin/sh
PROG=${0##*/}
if [ $# = 2 ]; then
	# for using same syntax as rpm own find-lang
	RPM_BUILD_ROOT=$1
	shift
fi
dir=$RPM_BUILD_ROOT@localedir@
langfile=$1
tmp=$(mktemp) || exit 1
rc=0

find $dir -name '*.pak' > $tmp

echo '%defattr(644,root,root,755)' > $langfile
while read file; do
	lang=${file##*/}
	lang=${lang%.pak}
	case "$lang" in
	zh-TW)
		lang=zh_TW
	;;
	zh-CN)
		lang=zh_CN
	;;
	en-US|en-GB)
		lang=en
	;;
	pt-BR)
		lang=pt_BR
	;;
	fr-CA)
		lang=fr_CA
	;;
	pt-PT)
		lang=pt
	;;
	es-419)
		lang=es_LA
	;;
	*-*)
		echo >&2 "ERROR: Need mapping for $lang!"
		rc=1
	;;
	esac
	echo "%lang($lang) ${file#$RPM_BUILD_ROOT}" >> $langfile
done < $tmp

if [ "$(grep -Ev '(^%defattr|^$)' $langfile | wc -l)" -le 0 ]; then
	echo >&2 "$PROG: Error: international files not found!"
	rc=1
fi

rm -f $tmp
exit $rc
