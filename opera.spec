# BRANCHES:
# - HEAD - stable version
# - DEVEL - development version
# - WEEKLY - weekly development version

# TODO:
# - drop stable and snap on this (WEEKLY) branch
# - move translations into a separate, noarch package
# - drop those dozens of if statements and use branches for different sources
#
%bcond_without	shared		# static or shared version
%bcond_without	distributable	# distributable or not
%bcond_without	incall		# include all tarballs into src.rpm (but splitted into shared/static)
%bcond_with	weekly		# weekly snapshot version

%ifarch sparc sparcv9
%undefine with_shared
%endif

%if %{with weekly}
%define	ver		9.23
%define	sver		%{ver}
%define	fix		%{nil}
%define	dirrel		20070809
%define	reltype		%{nil}
%define	magicstr	660
%define	with_snap	1
%else
%define	ver		9.50
%define	sver		9.50b2
%define	fix		b2
%define	dirrel		20080422
%define	reltype		final
%define	magicstr	1933
%endif

%define	shver		%(echo %{ver} | tr -d .)%{fix}
%define	x86_shared_rel		%{dirrel}.5
%define	x86_static_rel		%{dirrel}.1
%define	sparc_shared_rel	%{dirrel}.2
%define	sparc_static_rel	%{dirrel}.1
%define	ppc_shared_rel		%{dirrel}.3
%define	ppc_static_rel		%{dirrel}.1
%if %{with shared}
%define	type		shared
# We should be able to build src.rpm also on not supported archs
%define	rel		%{x86_shared_rel}
%ifarch sparc sparcv9
#%%define	rel		%{sparc_shared_rel}
%define	rel		%{sparc_static_rel}
%else
%ifarch ppc
%define	rel		%{ppc_shared_rel}
%endif
%endif
%else
%define	type		static
%define	rel		%{x86_static_rel}
%ifarch sparc sparcv9
%define	rel		%{sparc_static_rel}
%else
%ifarch ppc
%define	rel		%{ppc_static_rel}
%endif
%endif
%endif

# define to 0 and then redefine to avoid
# not defined macros
%define	need_ix86_shared_snap	0
%define	need_sparc_shared_snap	0
%define	need_ppc_shared_snap	0
%define	need_ix86_static_snap	0
%define	need_sparc_static_snap	0
%define	need_ppc_static_snap	0

%define	need_ix86_shared	0
%define	need_sparc_shared	0
%define	need_ppc_shared		0
%define	need_ix86_static	0
%define	need_sparc_static	0
%define	need_ppc_static		0

%if %{with incall}
#	with incall?	[if]
%if	%{with snap}
#		with snap?	[if]
%if	%{with shared}
#			with shared?	[if]
%define	need_ix86_shared_snap	1
%define	need_sparc_shared_snap	0
%define	need_ppc_shared_snap	1
%else
#			with shared:	[else]
%define	need_ix86_static_snap	1
%define	need_sparc_static_snap	1
%define	need_ppc_static_snap	1
%endif
#			with shared;	[endif]
%else
#		with snap:	[else]
%if %{with shared}
#			with shared?	[if]
%define	need_ix86_shared	1
#%%define	need_sparc_shared	1
%define	need_sparc_static	1
%define	need_ppc_shared	1
%else
#			with shared:	[else]
%define	need_ix86_static	1
%define	need_sparc_static	1
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
%else
#		is ix86:	[else]
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
#%%define	need_sparc_shared	1
%define	need_sparc_static	1
%else
#				with shared:	[else]
%define	need_sparc_static	1
%endif
#				with shared;	[endif]
%endif
#			with snap;	[endif]
%else
#		is sparc:	[else]
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
#				with shared;	[endif]
%endif
#			with snap;	[endif]
%endif
#		is ppc;		[endif]
%endif
#		is sparc;	[endif]
%endif
#		is ix86;	[endif]
%endif
#	with incall;	[endif]

%if %{with weekly}
%define	need_ppc_shared_snap	0
%define	need_ppc_static_snap	0
%define	need_sparc_shared_snap	0
%define	need_sparc_static_snap	0
%endif

%define		_rel	1
Summary:	World fastest web browser
Summary(pl.UTF-8):	Najszybsza przeglądarka WWW na świecie
Name:		opera
Version:	%{ver}%{fix}
Release:	%{?with_snap:1.%{rel}.}%{_rel}
Epoch:		2
License:	Distributable for PLD until 31 Dec 2006 - http://distribute.opera.com/ (otherwise restricted, see file LICENSE)
Group:		X11/Applications/Networking

%if %{need_ix86_static}
Source0:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/i386/static/%{name}-%{sver}-%{x86_static_rel}-static-qt.i386-en.tar.bz2
# Source0-md5:	0c721abff854df6c8ec7746956a37f55
%{!?with_distributable:NoSource:	0}
%endif

%if %{need_ix86_static_snap}
%if %{with weekly}
Source30100:	http://snapshot.opera.com/unix/Weekly-%{magicstr}/intel-linux/%{name}-%{sver}-%{x86_static_rel}-static-qt.i386-en-%{magicstr}.tar.bz2
%else
Source100:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/intel-linux/%{name}-%{sver}-%{x86_static_rel}-static-qt.i386-en-%{magicstr}.tar.bz2
%endif
%{!?with_distributable:NoSource:	100}
%endif

%if %{need_sparc_static}
Source1:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/sparc/static/%{name}-%{sver}-%{sparc_static_rel}-static-qt.sparc-en.tar.bz2
# Source1-md5:	98a84755df7d74812e8b8fa20d09d929
%{!?with_distributable:NoSource:	1}
%endif

%if %{need_sparc_static_snap}
Source101:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/%{magicstr}/sparc-linux/%{name}-%{sver}-%{sparc_static_rel}-static-qt.sparc-en.tar.bz2
# Source101-md5:	913ccb28106f9f5acd3d94c8dc71ae1
%{!?with_distributable:NoSource:	101}
%endif

%if %{need_ppc_static}
Source2:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/ppc/static/%{name}-%{sver}-%{ppc_static_rel}-static-qt.ppc-en.tar.bz2
# Source2-md5:	132fa2d85a2e0c2840b8bf2d27cfc93d
%{!?with_distributable:NoSource:	2}
%endif

%if %{need_ppc_static_snap}
%if %{with weekly}
Source30102:	http://snapshot.opera.com/unix/Weekly-%{magicstr}/ppc-linux/%{name}-%{sver}-%{ppc_static_rel}-static-qt.ppc-en-%{magicstr}.tar.bz2
%else
Source102:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/%{magicstr}/ppc-linux/%{name}-%{sver}-%{ppc_static_rel}-static-qt.ppc-en.tar.bz2
%endif
%{!?with_distributable:NoSource:	102}
%endif

%if %{need_ix86_shared}
Source20:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/i386/shared/%{name}-%{sver}-%{x86_shared_rel}-shared-qt.i386-en.tar.bz2
# Source20-md5:	1a8e824eb39baa1c05018aa6a8d823c8
%{!?with_distributable:NoSource:	20}
%endif

%if %{need_ix86_shared_snap}
%if %{with weekly}
Source301020:	http://snapshot.opera.com/unix/Weekly-%{magicstr}/intel-linux/%{name}-%{sver}-%{x86_shared_rel}-shared-qt.i386-en-%{magicstr}.tar.bz2
# Source301020-md5:	fe3c699c4509788276a94e325cd1bc5b
%else
Source1020:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/intel-linux/%{name}-%{sver}-%{x86_shared_rel}-shared-qt.i386-%{magicstr}.tar.bz2
# Source1020-md5:	8655d3c4623db40076507f03987158ae
%{!?with_distributable:NoSource:	1020}
%endif
%endif

%if %{need_sparc_shared}
Source21:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/sparc/shared/gcc-2.95/%{name}-%{sver}-%{sparc_shared_rel}-shared-qt.sparc-en.tar.bz2
# Source21-md5:	883df8058672cf52678a07d714dcfce
%{!?with_distributable:NoSource:	21}
%endif

%if %{need_sparc_shared_snap}
Source1021:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/%{magicstr}/sparc-linux/%{name}-%{sver}-%{sparc_shared_rel}-shared-qt.sparc-en.tar.bz2
# Source1021-md5:	e190021f5530de3f711006cd9f6bb339
%{!?with_distributable:NoSource:	1021}
%endif

%if %{need_ppc_shared}
Source22:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/ppc/shared/gcc-2.95/%{name}-%{sver}-%{ppc_shared_rel}-shared-qt.ppc-en.tar.bz2
# Source22-md5:	2f9bf50540fac7ed63f2984a13b1010d
%{!?with_distributable:NoSource:	22}
%endif

%if %{need_ppc_shared_snap}
%if %{with weekly}
Source301022:	http://snapshot.opera.com/unix/Weekly-%{magicstr}/ppc-linux/%{name}-%{sver}-%{ppc_shared_rel}-shared-qt.ppc-en-%{magicstr}.tar.bz2
# Source301022-md5:	65293d788e18d0c23cccac71b9fe567c
%else
Source1022:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/ppc-linux/%{name}-%{sver}-%{ppc_shared_rel}-shared-qt.ppc-%{magicstr}.tar.bz2
# Source1022-md5:	94b4d77cdcdf42a40ebe2d682892bb9a
%{!?with_distributable:NoSource:	1022}
%endif
%endif

Source4:	%{name}.desktop
Patch0:		%{name}-wrapper.patch
URL:		http://www.opera.com/
BuildRequires:	rpmbuild(macros) >= 1.356
BuildRequires:	sed >= 4.0
Requires:	browser-plugins >= 2.0
Requires:	freetype >= 2
Provides:	wwwbrowser
ExclusiveArch:	%{ix86} %{x8664} ppc sparc sparcv9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/opera/plugins
%define		_operadocdir	%{_docdir}/%{name}-%{ver}

%description
Opera is world fastest web browser. It supports most of nowaday
extensions of HTML. And it is quite stable. This version is %{?with_shared:shared}%{!?with_shared:statically}
linked with Qt.

%description -l pl.UTF-8
Opera jest najszybszą przeglądarką WWW na świecie. Obsługuje większość
dzisiejszych rozszerzeń HTML-a. Dodatkowo jest w miarę stabilna. Ta
wersja jest skonsolidowana %{?with_shared:dynamicznie}%{!?with_shared:statycznie} z Qt.

%prep
%ifarch %{ix86}
%setup -q -T -b %{?with_weekly:30}%{?with_snap:10}%{?with_shared:2}0 -n %{name}-%{ver}-%{rel}-%{type}-qt.i386%{?magicstr:-%{magicstr}}
%endif
%ifarch sparc sparcv9
%setup -q -T -b %{?with_weekly:30}%{?with_snap:10}%{?with_shared:2}1 -n %{name}-%{ver}-%{rel}-%{type}-qt.sparc%{?magicstr:-%{magicstr}}
%endif
%ifarch ppc
%setup -q -T -b %{?with_weekly:30}%{?with_snap:10}%{?with_shared:2}2 -n %{name}-%{ver}-%{rel}-%{type}-qt.ppc%{?magicstr:-%{magicstr}}
%endif
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_sysconfdir}}

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/plugins -b <<'EOF'
# opera does not use for .xpt files
*.xpt

# use mplayerplug-in-opera instead
mplayerplug-in*

# opera uses libjava.so to run java
libjavaplugin_oji.so
EOF

sh install.sh \
	DESTDIR=$RPM_BUILD_ROOT \
	--prefix=%{_prefix} \
	--exec_prefix=%{_libdir}/%{name}/bin \
	--plugindir=%{_libdir}/%{name}/plugins \
	--docdir=%{_operadocdir}

# install in kde etc.
install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}

install etc/* $RPM_BUILD_ROOT%{_sysconfdir}
install usr/share/pixmaps/*.xpm $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%doc LICENSE
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/opera*rc*

# browser plugins v2
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/opera
%dir %{_libdir}/opera/bin
%attr(755,root,root) %{_libdir}/opera/bin/*
%dir %{_plugindir}
%dir %{_datadir}/opera
%{_datadir}/opera/*.*
%{_datadir}/opera/ini
%{_datadir}/opera/java
%{_datadir}/opera/skin
%{_datadir}/opera/styles
%dir %{_datadir}/opera/locale
%{_datadir}/opera/locale/en
%{_datadir}/opera/locale/english.lng
%{_desktopdir}/*.desktop
%{_mandir}/man1/opera.1*
%{_pixmapsdir}/opera.xpm
