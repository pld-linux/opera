# TODO:
# - move translations into a separate, noarch package
#
%bcond_without	shared		# static or shared version
%bcond_without	distributable	# distributable or not
%bcond_without	incall		# include all tarballs into src.rpm (but splitted into shared/static)
%bcond_with	snap		# snap version

%if %{with snap}
%define	ver		7.60
%define dirrel		20041026
%define reltype         Preview-2
%else
%define ver             7.54
%define dirrel          20040803
%define reltype         final
%endif

%define shver		%(echo %{ver} | tr -d .)
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

# define to 0 and then redefine to avoid
# not defined macros
%define need_ix86_shared_snap	0
%define need_sparc_shared_snap	0
%define need_ppc_shared_snap	0
%define need_ix86_static_snap	0
%define need_sparc_static_snap	0
%define need_ppc_static_snap	0

%define need_ix86_shared	0
%define need_sparc_shared	0
%define need_ppc_shared		0
%define need_ix86_static	0
%define need_sparc_static	0
%define need_ppc_static		0

%if %{with incall}
#	with incall?	[if]
%if	%{with snap}
#		with snap?	[if]
%if	%{with shared}
#			with shared?	[if]
%define	need_ix86_shared_snap	1
%define need_sparc_shared_snap	1
%define	need_ppc_shared_snap	1
%else
#			with shared:	[else]
%define	need_ix86_static_snap	1
%define need_sparc_static_snap	1
%define	need_ppc_static_snap	1
%endif
#			with shared;	[endif]
%else
#		with snap:	[else]
%if %{with shared}
#			with shared?	[if]
%define	need_ix86_shared	1
%define need_sparc_shared	1
%define	need_ppc_shared	1
%else
#			with shared:	[else]
%define	need_ix86_static	1
%define need_sparc_static	1
%define	need_ppc_static	1
%endif
#			with shared;	[endif]
%endif
#		with snap;	[endif]
%else
#	with incall:	[else]
%ifarch	%{ix86}
#		is ix86?	[if]
%if	%{with snap}
#			with snap?	[if]
%if	%{with shared}
#				with shared?	[if]
%define	need_ix86_shared_snap	1
%else
#				with shared:	[else]
%define	need_ix86_static_snap	1
%endif
#				with shared;	[endif]
%else
#			with snap:	[else]
%if	%{with shared}
#				with shared?	[if]
%define	need_ix86_shared	1
%else
#				with shared:	[else]
%define	need_ix86_static	1
%endif
#				with shared;	[endif]
%endif
#			with snap;	[endif]
%endif
#		is ix86;	[endif]
%ifarch	sparc sparc64
#		is sparc?	[if]
%if	%{with snap}
#			with snap?	[if]
%if	%{with shared}
#				with shared?	[if]
%define	need_sparc_shared_snap	1
%else
#				with shared:	[else]
%define	need_sparc_static_snap	1
%endif
#				with shared;	[endif]
%else
#			with snap:	[else]
%if	%{with shared}
#				with shared?	[if]
%define	need_sparc_shared	1
%else
#				with shared:	[else]
%define	need_sparc_static	1
%endif
#				with shared;	[endif]
%endif
#			with snap;	[endif]
%endif
#		is sparc;	[endif]
%ifarch	ppc
#		is ppc?		[if]
%if	%{with snap}
#			with snap?	[if]
%if	%{with shared}
#				with shared?	[if]
%define	need_ppc_shared_snap	1
%else
#				with shared:	[else]
%define	need_ppc_static_snap	1
%endif
#				with shared;	[endif]
%else
#			with snap:	[else]
%if	%{with shared}
#				with shared?	[if]
%define	need_ppc_shared	1
%else
#				with shared:	[else]
%define	need_ppc_static	1
%endif
#				with shared;	[endif
%endif
#			with snap;	[endif
%endif
#		is ppc;		[endif]
%endif
#	with incall;	[endif]

Summary:	World fastest web browser
Summary(pl):	Najszybsza przegl±darka WWW na ¶wiecie
Name:		opera
Version:	%{ver}%{?with_snap:.%{rel}}
Release:	4
Epoch:		1
License:	Distributable for PLD until 31 Dec 2006 - http://distribute.opera.com/ (otherwise restricted, see file LICENSE)
Group:		X11/Applications/Networking

%if %{need_ix86_static}
Source0:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/i386/static/%{name}-%{ver}-%{x86_static_rel}-static-qt.i386-en.tar.bz2
# Source0-md5:	0a7e933ef593d4b7a897041c9f87bba2
%{!?with_distributable:NoSource:	0}
%endif

%if %{need_ix86_static_snap}
Source100:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/intel-linux/en/%{name}-%{ver}-%{x86_static_rel}-static-qt.i386-en.tar.bz2
%{!?with_distributable:NoSource:	100}
%endif

%if %{need_sparc_static}
Source1:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/sparc/static/%{name}-%{ver}-%{sparc_static_rel}-static-qt.sparc-en.tar.bz2
# Source1-md5:	04976a6ace7a4345ce5e4cf763159939
%{!?with_distributable:NoSource:	1}
%endif

%if %{need_sparc_static_snap}
Source101:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/sparc-linux/en/%{name}-%{ver}-%{sparc_static_rel}-static-qt.sparc-en.tar.bz2
# Source101-md5:  04976a6ace7a4345ce5e4cf763159939
%{!?with_distributable:NoSource:	101}
%endif

%if %{need_ppc_static}
Source2:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/ppc/static/%{name}-%{ver}-%{ppc_static_rel}-static-qt.ppc-en.tar.bz2
# Source2-md5:	c11a4c78d18bdaa4bd338b4c0dc27f38
%{!?with_distributable:NoSource:	2}
%endif

%if %{need_ppc_static_snap}
Source102:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/ppc-linux/en/%{name}-%{ver}-%{ppc_static_rel}-static-qt.ppc-en.tar.bz2
%{!?with_distributable:NoSource:	102}
%endif

%if %{need_ix86_shared}
Source20:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/i386/shared/%{name}-%{ver}-%{x86_shared_rel}-shared-qt.i386-en.tar.bz2
# Source20-md5:	0e407a050f3aa4559011a3cea707cd20
%{!?with_distributable:NoSource:	20}
%endif

%if %{need_ix86_shared_snap}
Source1020:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/intel-linux/en/%{name}-%{ver}-%{x86_shared_rel}-shared-qt.i386-en.tar.bz2
# Source1020-md5:	a7938217483f89de6ad7c43ca4e13fb4
%{!?with_distributable:NoSource:	1020}
%endif

%if %{need_sparc_shared}
Source21:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/sparc/shared/gcc-2.95/%{name}-%{ver}-%{sparc_shared_rel}-shared-qt.sparc-en.tar.bz2
# Source21-md5:	d8635013dac0c98c680997fcc9dd66c4
%{!?with_distributable:NoSource:	21}
%endif

%if %{need_ix86_shared_snap}
Source1021:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/sparc-linux/en/%{name}-%{ver}-%{sparc_shared_rel}-shared-qt.sparc-en.tar.bz2
# Source1021-md5:	487538aeb49d5a17f92e82fd5c5443d9
%{!?with_distributable:NoSource:	1021}
%endif

%if %{need_ppc_shared}
Source22:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/ppc/shared/gcc-2.95/%{name}-%{ver}-%{ppc_shared_rel}-shared-qt.ppc-en.tar.bz2
# Source22-md5:	516992e68c5a710d795a1ecc791c7f4d
%{!?with_distributable:NoSource:	22}
%endif

%if %{need_ppc_shared_snap}
Source1022:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/ppc-linux/en/%{name}-%{ver}-%{ppc_shared_rel}-shared-qt.ppc-en.tar.bz2
# Source1022-md5:	b69d2ed1ca94ecc612fe0b8fbf4b1beb
%{!?with_distributable:NoSource:	1022}
%endif

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
dzisiejszych rozszerzeñ HTML-a. Dodatkowo jest w miarê stabilna. Jedyn±
niedogodno¶ci± s± reklamy ukazuj±ce siê w górze okna. Wersja
statycznie skonsolidowana z qt.

%prep
%ifarch %{ix86}
%setup -q -T -b %{?with_snap:10}%{?with_shared:2}0 -n %{name}-%{ver}-%{rel}-%{type}-qt.i386-en
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

%dir %{_datadir}/opera/locale
%{_datadir}/opera/locale/en
%{_datadir}/opera/locale/english.lng

%{_pixmapsdir}/opera.xpm
%{_desktopdir}/*.desktop

%{_mandir}/man1/opera.1*
