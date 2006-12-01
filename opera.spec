# TODO:
# - move translations into a separate, noarch package
#
%bcond_without	shared		# static or shared version
%bcond_without	distributable	# distributable or not
%bcond_without	incall		# include all tarballs into src.rpm (but splitted into shared/static)
%bcond_with	snap		# snap version
%bcond_with	weekly		# weekly snapshot version

%ifarch sparc64 sparc
%undefine with_shared
%endif

%if %{with weekly}
%define	ver		9.10
%define	sver		%{ver}
%define	fix		%{nil}
%define	dirrel		20061201
%define	magicstr	505
%define with_snap	1
%else
%if %{with snap}
%define	ver		9.0
%define	sver		%{ver}
%define	fix		%{nil}
%define	dirrel		20060206
%define	reltype		Preview-2
%define	magicstr	%{nil}
%else
%define	ver		9.02
%define	sver		9.02
%define	fix		%{nil}
%define	dirrel		20060919
%define	reltype		final
%define	magicstr	434
%endif
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
%ifarch sparc64 sparc
#%%define	rel		%{sparc_shared_rel}
%define	rel		%{sparc_static_rel}
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
#%%define	need_sparc_shared	1
%define	need_sparc_static	1
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

%define		_rel	3
Summary:	World fastest web browser
Summary(pl):	Najszybsza przegl±darka WWW na ¶wiecie
Name:		opera
Version:	%{ver}%{fix}
Release:	%{?with_snap:1.%{rel}.}%{_rel}
Epoch:		2
License:	Distributable for PLD until 31 Dec 2006 - http://distribute.opera.com/ (otherwise restricted, see file LICENSE)
Group:		X11/Applications/Networking

%if %{need_ix86_static}
Source0:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/i386/static/%{name}-%{sver}-%{x86_static_rel}-static-qt.i386-en.tar.bz2
# Source0-md5:	d6c5eb5fa495fedb60b48d98daf365c3
%{!?with_distributable:NoSource:	0}
%endif

%if %{need_ix86_static_snap}
%if %{with weekly}
Source30100:	http://snapshot.opera.com/unix/Weekly-%{magicstr}/intel-linux/%{name}-%{sver}-%{x86_static_rel}-static-qt.i386-en-%{magicstr}.tar.bz2
%else
Source100:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/%{magicstr}/intel-linux/%{name}-%{sver}-%{x86_static_rel}-static-qt.i386-en-%{magicstr}.tar.bz2
%endif
%{!?with_distributable:NoSource:	100}
%endif

%if %{need_sparc_static}
Source1:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/sparc/static/%{name}-%{sver}-%{sparc_static_rel}-static-qt.sparc-en.tar.bz2
# Source1-md5:	6b15ff08f9f5a2f13821cf00e3ca63b2
%{!?with_distributable:NoSource:	1}
%endif

%if %{need_sparc_static_snap}
Source101:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/%{magicstr}/sparc-linux/%{name}-%{sver}-%{sparc_static_rel}-static-qt.sparc-en.tar.bz2
# Source101-md5:	913ccb28106f9f5acd3d94c8dc71ae1
%{!?with_distributable:NoSource:	101}
%endif

%if %{need_ppc_static}
Source2:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/ppc/static/%{name}-%{sver}-%{ppc_static_rel}-static-qt.ppc-en.tar.bz2
# Source2-md5:	6bacc32a3ce81a2fb94c22860e772f8b
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
# Source20-md5:	327d0bf1f3c4eedd47b444b36c9091f6
%{!?with_distributable:NoSource:	20}
%endif

%if %{need_ix86_shared_snap}
%if %{with weekly}
Source301020:	http://snapshot.opera.com/unix/Weekly-%{magicstr}/intel-linux/%{name}-%{sver}-%{x86_shared_rel}-shared-qt.i386-en-%{magicstr}.tar.bz2
# Source301020-md5:	e1fec5d7a0ab7445856a17ac534e45ce
%else
Source1020:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/%{magicstr}/intel-linux/%{name}-%{sver}-%{x86_shared_rel}-shared-qt.i386-en.tar.bz2
# Source1020-md5:	6f296be6b9fc3001588d4509016062bd
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
# Source22-md5:	801b94f1a98f4a953fa11ea1c1b4cb33
%{!?with_distributable:NoSource:	22}
%endif

%if %{need_ppc_shared_snap}
%if %{with weekly}
Source301022:	http://snapshot.opera.com/unix/Weekly-%{magicstr}/ppc-linux/%{name}-%{sver}-%{ppc_shared_rel}-shared-qt.ppc-en-%{magicstr}.tar.bz2
# Source301022-md5:	65293d788e18d0c23cccac71b9fe567c
%else
Source1022:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/%{magicstr}/ppc-linux/%{name}-%{sver}-%{ppc_shared_rel}-shared-qt.ppc-en.tar.bz2
# Source1022-md5:	74985fa6da49b2e54c9d03dab1119325
%{!?with_distributable:NoSource:	1022}
%endif
%endif

Source4:	%{name}.desktop
Patch0:		%{name}-wrapper.patch
URL:		http://www.opera.com/
BuildRequires:	sed >= 4.0
Requires:	freetype >= 2
Provides:	wwwbrowser
ExclusiveArch:	%{ix86} ppc sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/opera/plugins
%define		_operadocdir	%{_docdir}/%{name}-%{ver}

%description
Opera is world fastest web browser. It supports most of nowaday
extensions of HTML. And it is quite stable. This version is %{?with_shared:shared}%{!?with_shared:statically}
linked with Qt.

%description -l pl
Opera jest najszybsz± przegl±dark± WWW na ¶wiecie. Obs³uguje wiêkszo¶æ
dzisiejszych rozszerzeñ HTML-a. Dodatkowo jest w miarê stabilna. Ta
wersja jest skonsolidowana %{?with_shared:dynamicznie}%{!?with_shared:statycznie} z Qt.

%prep
%ifarch %{ix86}
%setup -q -T -b %{?with_weekly:30}%{?with_snap:10}%{?with_shared:2}0 -n %{name}-%{sver}-%{rel}-%{type}-qt.i386-en%{?magicstr:-%{magicstr}}
%endif
%ifarch sparc sparc64
%setup -q -T -b %{?with_weekly:30}%{?with_snap:10}%{?with_shared:2}1 -n %{name}-%{sver}-%{rel}-%{type}-qt.sparc-en%{?magicstr:-%{magicstr}}
%endif
%ifarch ppc
%setup -q -T -b %{?with_weekly:30}%{?with_snap:10}%{?with_shared:2}2 -n %{name}-%{sver}-%{rel}-%{type}-qt.ppc-en%{?magicstr:-%{magicstr}}
%endif
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},%{_sysconfdir}}

sh install.sh \
	DESTDIR=$RPM_BUILD_ROOT \
	--prefix=%{_prefix} \
	--exec_prefix=%{_libdir}/opera/bin \
	--docdir=%{_operadocdir}

# install in kde etc.
install images/opera.xpm $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}

mv -f $RPM_BUILD_ROOT%{_datadir}/%{name}/config/* $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/opera*rc*
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/opera
%dir %{_libdir}/opera/bin
%attr(755,root,root) %{_libdir}/opera/bin/*
%dir %{_plugindir}
%attr(755,root,root) %{_plugindir}/*
%dir %{_datadir}/opera
%{_datadir}/opera/*.*
%{_datadir}/opera/images
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
