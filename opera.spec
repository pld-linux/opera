# TODO:
#	move translations into a separate, noarch package
#
%bcond_without	shared		# static or shared version
%bcond_without	distributable	# distributable or not
%bcond_without	incall		# include all tarballs into src.rpm (but splitted into shared/static)
%bcond_with	snap		# snap version

%define	ver		7.54
%define shver		%(echo %{ver} | tr -d .)
%define	dirrel		20040803
# type of release, usually final or beta or Preview-4 for snaps
%define	reltype		final
%define	x86_shared_rel		%{dirrel}.5
%define	x86_static_rel		%{dirrel}.1
%define	sparc_shared_rel	%{dirrel}.2
%define	sparc_static_rel	%{dirrel}.1
%define	ppc_shared_rel		%{dirrel}.2
%define	ppc_static_rel		%{dirrel}.1
%if %{with shared}
%define	type		shared
# We should be able to build src.rpm also on not supported archs
%define	rel		%{x86_shared_rel}
%ifarch sparc64 sparc
%define	rel		%{sparc_shared_rel}
%endif
%ifarch ppc
%define	rel		%{ppc_shared_rel}
%endif
%else
%define	type		static
%define	rel		%{x86_static_rel}
%ifarch sparc sparc64
%define	rel		%{sparc_static_rel}
%endif
%ifarch ppc
%define	rel		%{ppc_static_rel}
%endif
%endif

Summary:	World fastest web browser
Summary(pl):	Najszybsza przegl±darka WWW na ¶wiecie
Name:		opera
Version:	%{ver}.%{rel}
Release:	2
License:	Distributable for PLD until 31 Dec 2006 - http://distribute.opera.com/ (otherwise restricted, see file LICENSE)
Group:		X11/Applications/Networking
%if %{without shared}
%{!?with_incall:%ifarch %{ix86}}
%if ! %{with snap}
Source0:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/i386/static/%{name}-%{ver}-%{x86_static_rel}-static-qt.i386-en.tar.bz2
# Source0-md5:	0a7e933ef593d4b7a897041c9f87bba2
%else
Source100:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/intel-linux/en/%{name}-%{ver}-%{x86_static_rel}-static-qt.i386-en.tar.bz2
%endif
%{!?with_distributable:NoSource:	0}
%if ! %{with incall}
%endif
%ifarch sparc sparc64
%endif
%if ! %{with snap}
Source1:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/sparc/static/%{name}-%{ver}-%{sparc_static_rel}-static-qt.sparc-en.tar.bz2
# Source1-md5:	04976a6ace7a4345ce5e4cf763159939
%else
Source101:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/sparc-linux/en/%{name}-%{ver}-%{sparc_static_rel}-static-qt.sparc-en.tar.bz2
%endif
%{!?with_distributable:NoSource:	1}
%if ! %{with incall}
%endif
%ifarch ppc
%endif
%if ! %{with snap}
Source2:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/ppc/static/%{name}-%{ver}-%{ppc_static_rel}-static-qt.ppc-en.tar.bz2
# Source2-md5:	c11a4c78d18bdaa4bd338b4c0dc27f38
%else
Source102:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/ppc-linux/en/%{name}-%{ver}-%{ppc_static_rel}-static-qt.ppc-en.tar.bz2
%endif
%{!?with_distributable:NoSource:	2}
%{!?with_incall:%endif}
%else
%{!?with_incall:%ifarch %{ix86}}
%if ! %{with snap}
Source20:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/i386/shared/%{name}-%{ver}-%{x86_shared_rel}-shared-qt.i386-en.tar.bz2
# Source20-md5:	0e407a050f3aa4559011a3cea707cd20
%else
Source1020:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/intel-linux/en/%{name}-%{ver}-%{x86_shared_rel}-shared-qt.i386-en.tar.bz2
%endif
%{!?with_distributable:NoSource:	20}
%if ! %{with incall}
%endif
%ifarch sparc sparc64
%endif
%if ! %{with snap}
Source21:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/sparc/shared/gcc-2.95/%{name}-%{ver}-%{sparc_shared_rel}-shared-qt.sparc-en.tar.bz2
# Source21-md5:	d8635013dac0c98c680997fcc9dd66c4
%else
Source1021:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/sparc-linux/en/%{name}-%{ver}-%{sparc_shared_rel}-shared-qt.sparc-en.tar.bz2
%endif
%{!?with_distributable:NoSource:	21}
%if ! %{with incall}
%endif
%ifarch ppc
%endif
%if ! %{with snap}
Source22:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/ppc/shared/gcc-2.95/%{name}-%{ver}-%{ppc_shared_rel}-shared-qt.ppc-en.tar.bz2
# Source22-md5:	516992e68c5a710d795a1ecc791c7f4d
%else
Source1022:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/ppc-linux/en/%{name}-%{ver}-%{ppc_shared_rel}-shared-qt.ppc-en.tar.bz2
%endif
%{!?with_distributable:NoSource:	22}
%endif
%{!?with_incall:%endif}
Source201:	ftp://ftp.opera.com/pub/opera/unix/lng/721/bg/ou721_480bg.lng
Source202:	ftp://ftp.opera.com/pub/opera/unix/lng/721/ca/ou721_480ca.lng
Source203:	ftp://ftp.opera.com/pub/opera/unix/lng/721/zh-cn/ou721_480zh-cn.lng
Source204:	ftp://ftp.opera.com/pub/opera/unix/lng/721/da/ou721_480da.lng
Source205:	ftp://ftp.opera.com/pub/opera/unix/lng/721/nl/ou721_480nl.lng
Source206:	ftp://ftp.opera.com/pub/opera/unix/lng/721/es-LA/ou721_480es-LA.lng
Source207:	ftp://ftp.opera.com/pub/opera/unix/lng/721/ja/ou721_480ja.lng
Source208:	ftp://ftp.opera.com/pub/opera/unix/lng/752/fi/ou752_727fi.lng
Source209:	ftp://ftp.opera.com/pub/opera/unix/lng/752/fr/ou752_727fr.lng
Source210:	ftp://ftp.opera.com/pub/opera/unix/lng/752/it/ou752_727it.lng
Source211:	ftp://ftp.opera.com/pub/opera/unix/lng/754/de/ou754_751de.lng
Source212:	ftp://ftp.opera.com/pub/opera/unix/lng/754/ko/ou754_751ko.lng
Source213:	ftp://ftp.opera.com/pub/opera/unix/lng/754/nb/ou754_751nb.lng
Source214:	ftp://ftp.opera.com/pub/opera/unix/lng/754/pl/ou754_751pl.lng
Source215:	ftp://ftp.opera.com/pub/opera/unix/lng/754/es-ES/ou754_751es-ES.lng
Source216:	ftp://ftp.opera.com/pub/opera/unix/lng/754/sv/ou754_751sv.lng
Source217:	ftp://ftp.opera.com/pub/opera/linux/lng/711/el/ou711_406el.lng
Source218:	http://www.opera.com/download/lng/linux-freebsd/ou711_406zh-tw.lng
Source219:	http://www.opera.com/download/lng/linux-freebsd/ou711_406en-GB.lng
Source220:	http://www.opera.com/download/lng/linux-freebsd/ou711_406nn.lng
Source221:	http://www.opera.com/download/lng/linux-freebsd/ou711_406pt-BR.lng
Source222:	http://www.opera.com/download/lng/linux-freebsd/ou711_406ru.lng
Source223:	http://www.opera.com/download/lng/linux-freebsd/ou711_406tr.lng
Source4:	%{name}.desktop
URL:		http://www.opera.com/
ExclusiveArch:	%{ix86} ppc sparc sparc64
Requires:	freetype >= 2

Requires:	openmotif >= 2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/opera/plugins
%define		_operadocdir	%{_docdir}/%{name}-%{ver}.%{rel}
%define		configfile	%{_datadir}/opera/config/opera6rc

%description
Opera is world fastest web browser. It supports most of nowaday
extensions of HTML. And it is quite stable. Only disadvantage are
advertisements on the top of its window. Version static linked with
qt.

%description -l pl
Opera jest najszybsz± przegl±dark± WWW na ¶wiecie. Obs³uguje wiêkszo¶æ
dzisiejszych rozszerzeñ HTMLa. Dodatkowo jest w miarê stabilna. Jedyn±
niedogodno¶ci± s± reklamy ukazuj±ce siê w górze okna. Wersja
statycznie skonsolidowana z qt.

%prep
%ifarch %{ix86}
%setup -q %{?with_shared:-T -b %{?with_snap:10}20} -n %{name}-%{ver}-%{rel}-%{type}-qt.i386-en
%endif
%ifarch sparc sparc64
%setup -q -T -b %{?with_snap:10}%{?with_shared:2}1 -n %{name}-%{ver}-%{rel}-%{type}-qt.sparc-en
%endif
%ifarch ppc
%setup -q -T -b %{?with_snap:10}%{?with_shared:2}2 -n %{name}-%{ver}-%{rel}-%{type}-qt.ppc-en
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/etc,%{_mandir}/man1,%{_pixmapsdir},%{_desktopdir}}

cat install.sh | sed 's|/etc|$RPM_BUILD_ROOT%{_sysconfdir}|' > install2.sh
mv install2.sh install.sh

echo y |\
sh install.sh \
  --prefix=$RPM_BUILD_ROOT%{_prefix} \
  --wrapperdir=$RPM_BUILD_ROOT%{_bindir} \
  --docdir=$RPM_BUILD_ROOT%{_operadocdir} \
  --sharedir=$RPM_BUILD_ROOT%{_datadir}/opera \
  --exec_prefix=$RPM_BUILD_ROOT%{_datadir}/opera/bin \
  --plugindir=$RPM_BUILD_ROOT%{_plugindir}

# Polish locale
install %{SOURCE201} $RPM_BUILD_ROOT%{_datadir}/opera/locale/bulgarian.lng
install %{SOURCE202} $RPM_BUILD_ROOT%{_datadir}/opera/locale/catalan.lng
install %{SOURCE203} $RPM_BUILD_ROOT%{_datadir}/opera/locale/chinese-simplified.lng
install %{SOURCE204} $RPM_BUILD_ROOT%{_datadir}/opera/locale/danish.lng
install %{SOURCE205} $RPM_BUILD_ROOT%{_datadir}/opera/locale/dutch.lng
install %{SOURCE206} $RPM_BUILD_ROOT%{_datadir}/opera/locale/spanish-latin-american.lng
install %{SOURCE207} $RPM_BUILD_ROOT%{_datadir}/opera/locale/japanese.lng
install %{SOURCE208} $RPM_BUILD_ROOT%{_datadir}/opera/locale/finish.lng
install %{SOURCE209} $RPM_BUILD_ROOT%{_datadir}/opera/locale/french.lng
install %{SOURCE210} $RPM_BUILD_ROOT%{_datadir}/opera/locale/italian.lng
install %{SOURCE211} $RPM_BUILD_ROOT%{_datadir}/opera/locale/germen.lng
install %{SOURCE212} $RPM_BUILD_ROOT%{_datadir}/opera/locale/korean.lng
install %{SOURCE213} $RPM_BUILD_ROOT%{_datadir}/opera/locale/norwegian-bokmal.lng
install %{SOURCE214} $RPM_BUILD_ROOT%{_datadir}/opera/locale/polish.lng
install %{SOURCE215} $RPM_BUILD_ROOT%{_datadir}/opera/locale/spanish.lng
install %{SOURCE216} $RPM_BUILD_ROOT%{_datadir}/opera/locale/swedish.lng
install %{SOURCE217} $RPM_BUILD_ROOT%{_datadir}/opera/locale/greek.lng
install %{SOURCE218} $RPM_BUILD_ROOT%{_datadir}/opera/locale/chinese-traditional.lng
install %{SOURCE219} $RPM_BUILD_ROOT%{_datadir}/opera/locale/english-british.lng
install %{SOURCE220} $RPM_BUILD_ROOT%{_datadir}/opera/locale/norwegian-nynorsk.lng
install %{SOURCE221} $RPM_BUILD_ROOT%{_datadir}/opera/locale/portuguese-brazilian.lng
install %{SOURCE222} $RPM_BUILD_ROOT%{_datadir}/opera/locale/russian.lng
install %{SOURCE223} $RPM_BUILD_ROOT%{_datadir}/opera/locale/turkish.lng

# man install
install man/opera.1 $RPM_BUILD_ROOT%{_mandir}/man1

# wrapper correction
sed s#$RPM_BUILD_ROOT## > $RPM_BUILD_ROOT%{_bindir}/opera2 $RPM_BUILD_ROOT%{_bindir}/opera
mv $RPM_BUILD_ROOT%{_bindir}/opera2 $RPM_BUILD_ROOT%{_bindir}/opera

# install in kde etc.
install images/opera.xpm $RPM_BUILD_ROOT%{_pixmapsdir}

install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}

# symlink który niweluje burkanie siê opery :>
#ln -sf %{_datadir}/opera/ $RPM_BUILD_ROOT/usr/share/
#ln -sf %{_libdir}/opera $RPM_BUILD_ROOT/usr/lib/

sed -i -e "s#$RPM_BUILD_ROOT##g" $RPM_BUILD_ROOT%{_datadir}/opera/java/*.policy

# always use wrapper linked with libXm.so.3
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/operamotifwrapper
ln -sf operamotifwrapper-3 $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/operamotifwrapper-2
ln -sf operamotifwrapper-3 $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/operamotifwrapper-1

# %{_libdir} is not the best place for it but opera doesn't search for it in better
# places :/
install lib/spellcheck.so $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE bugreport help
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/opera
%dir %{_datadir}/opera/bin
%attr(755,root,root) %{_datadir}/opera/bin/*
%{_datadir}/opera/config
%{_datadir}/opera/help
%{_datadir}/opera/images
%{_datadir}/opera/java
%dir %{_datadir}/opera/locale
%lang(bg) %{_datadir}/opera/locale/bulgarian.lng
%lang(ca) %{_datadir}/opera/locale/catalan.lng
%lang(da) %{_datadir}/opera/locale/danish.lng
%lang(de) %{_datadir}/opera/locale/german.lng
%lang(el) %{_datadir}/opera/locale/greek.lng
%lang(en_GB) %{_datadir}/opera/locale/english-british.lng
%lang(es) %{_datadir}/opera/locale/spanish.lng
%lang(es) %{_datadir}/opera/locale/spanish-latin-american.lng
%lang(fi) %{_datadir}/opera/locale/finish.lng
%lang(fr) %{_datadir}/opera/locale/french.lng
%lang(it) %{_datadir}/opera/locale/italian.lng
%lang(ja) %{_datadir}/opera/locale/japanese.lng
%lang(ko) %{_datadir}/opera/locale/korean.lng
%lang(nb) %{_datadir}/opera/locale/norwegian-bokmal.lng
%lang(nl) %{_datadir}/opera/locale/dutch.lng
%lang(nn) %{_datadir}/opera/locale/norwegian-nynorsk.lng
%lang(pl) %{_datadir}/opera/locale/polish.lng
%lang(pt_BR) %{_datadir}/opera/locale/portuguese-brazilian.lng
%lang(ru) %{_datadir}/opera/locale/russian.lng
%lang(sv) %{_datadir}/opera/locale/swedish.lng
%lang(tr) %{_datadir}/opera/locale/turkish.lng
%lang(zh_CN) %{_datadir}/opera/locale/chinese-simplified.lng
%lang(zh_TW) %{_datadir}/opera/locale/chinese-traditional.lng
%{_datadir}/opera/skin
%{_datadir}/opera/styles
%{_datadir}/opera/ini
%{_datadir}/opera/search.ini
%{_datadir}/opera/*.html
%{_datadir}/opera/*.ssr
%{_datadir}/opera/*.txt
%ifarch %{ix86}
%attr(755,root,root) %{_datadir}/opera/chartables.bin
%endif
%ifarch ppc
%attr(755,root,root) %{_datadir}/opera/chartables-be.bin
%endif
%attr(755,root,root) %{_datadir}/opera/opera6.adr
%attr(755,root,root) %{_libdir}/*.so
%dir %{_libdir}/opera
%dir %{_plugindir}
%attr(755,root,root) %{_plugindir}/*

%{_pixmapsdir}/opera.xpm
%{_desktopdir}/*.desktop

%{_mandir}/man1/opera.1*
