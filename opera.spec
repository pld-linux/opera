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
%define	ver		9.0
%define	sver		%{ver}
%define	fix		%{nil}
%define	dirrel		20060518
%define	magicstr	284
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
%define	ver		9.00
%define	sver		9.0
%define	magicstr	284
%define	fix		%{nil}
%define	dirrel		20060518
%define	reltype		beta2
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

Summary:	World fastest web browser
Summary(pl):	Najszybsza przegl±darka WWW na ¶wiecie
Name:		opera
Version:	%{ver}%{fix}
Release:	%{?with_snap:1.%{rel}.}1
Epoch:		2
License:	Distributable for PLD until 31 Dec 2006 - http://distribute.opera.com/ (otherwise restricted, see file LICENSE)
Group:		X11/Applications/Networking

%if %{need_ix86_static}
Source0:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/i386/static/%{name}-%{sver}-%{x86_static_rel}-static-qt.i386-en-%{magicstr}.tar.bz2
# Source0-md5:	54a29d830506e6c9381a305e0353055c
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
Source1:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/sparc/static/%{name}-%{sver}-%{sparc_static_rel}-static-qt.sparc-en-%{magicstr}.tar.bz2
# Source1-md5:	201c1927677939ab596f8c940f9fd059
%{!?with_distributable:NoSource:	1}
%endif

%if %{need_sparc_static_snap}
Source101:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/%{magicstr}/sparc-linux/%{name}-%{sver}-%{sparc_static_rel}-static-qt.sparc-en.tar.bz2
# Source101-md5:	913ccb28106f9f5acd3d94c8dc71ae1
%{!?with_distributable:NoSource:	101}
%endif

%if %{need_ppc_static}
Source2:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/ppc/static/%{name}-%{sver}-%{ppc_static_rel}-static-qt.ppc-en-%{magicstr}.tar.bz2
# Source2-md5:	b86bbd1b1ca2e146c30bfedcbe4403d0
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
Source20:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/i386/shared/%{name}-%{sver}-%{x86_shared_rel}-shared-qt.i386-en-%{magicstr}.tar.bz2
# Source20-md5:	4ea4938d39ae8c29c44208b246501cf6
%{!?with_distributable:NoSource:	20}
%endif

%if %{need_ix86_shared_snap}
%if %{with weekly}
Source301020:	http://snapshot.opera.com/unix/Weekly-%{magicstr}/intel-linux/%{name}-%{sver}-%{x86_shared_rel}-shared-qt.i386-en-%{magicstr}.tar.bz2
# Source301020-md5:	4ea4938d39ae8c29c44208b246501cf6
%else
Source1020:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/%{magicstr}/intel-linux/%{name}-%{sver}-%{x86_shared_rel}-shared-qt.i386-en.tar.bz2
# Source1020-md5:	6f296be6b9fc3001588d4509016062bd
%{!?with_distributable:NoSource:	1020}
%endif
%endif

%if %{need_sparc_shared}
Source21:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/sparc/shared/gcc-2.95/%{name}-%{sver}-%{sparc_shared_rel}-shared-qt.sparc-en-%{magicstr}.tar.bz2
# Source21-md5:	883df8058672cf52678a07d714dcfce
%{!?with_distributable:NoSource:	21}
%endif

%if %{need_sparc_shared_snap}
Source1021:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/%{magicstr}/sparc-linux/%{name}-%{sver}-%{sparc_shared_rel}-shared-qt.sparc-en.tar.bz2
# Source1021-md5:	e190021f5530de3f711006cd9f6bb339
%{!?with_distributable:NoSource:	1021}
%endif

%if %{need_ppc_shared}
Source22:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/ppc/shared/gcc-2.95/%{name}-%{sver}-%{ppc_shared_rel}-shared-qt.ppc-en-%{magicstr}.tar.bz2
# Source22-md5:	32c82535e3b1ea2b49389b4aa289234f
%{!?with_distributable:NoSource:	22}
%endif

%if %{need_ppc_shared_snap}
%if %{with weekly}
Source301022:	http://snapshot.opera.com/unix/Weekly-%{magicstr}/ppc-linux/%{name}-%{sver}-%{ppc_shared_rel}-shared-qt.ppc-en-%{magicstr}.tar.bz2
# Source301022-md5:	4ef11bec6221d79e30dfbbf76ff89fa3
%else
Source1022:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/%{magicstr}/ppc-linux/%{name}-%{sver}-%{ppc_shared_rel}-shared-qt.ppc-en.tar.bz2
# Source1022-md5:	74985fa6da49b2e54c9d03dab1119325
%{!?with_distributable:NoSource:	1022}
%endif
%endif

Source4:	%{name}.desktop

URL:		http://www.opera.com/
BuildRequires:	sed >= 4.0
Requires:	freetype >= 2
%{!?with_snap:Requires:	openmotif >= 2}
Provides:	wwwbrowser
ExclusiveArch:	%{ix86} ppc sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/opera/plugins
%define		_operadocdir	%{_docdir}/%{name}-%{ver}.%{rel}
%define		configfile	%{_datadir}/opera/config/opera6rc

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
%setup -q -T -b %{?with_weekly:30}%{?with_snap:10}%{?with_shared:2}0 -n %{name}-%{sver}-%{rel}-%{type}-qt.i386-en-%{magicstr}
%endif
%ifarch sparc sparc64
%setup -q -T -b %{?with_weekly:30}%{?with_snap:10}%{?with_shared:2}1 -n %{name}-%{sver}-%{rel}-%{type}-qt.sparc-en
%endif
%ifarch ppc
%setup -q -T -b %{?with_weekly:30}%{?with_snap:10}%{?with_shared:2}2 -n %{name}-%{sver}-%{rel}-%{type}-qt.ppc-en-%{magicstr}
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/etc,%{_libdir},%{_mandir}/man1,%{_pixmapsdir},%{_desktopdir}}
ln -s $RPM_BUILD_ROOT/etc  $RPM_BUILD_ROOT%{_prefix}/etc

sed -i -e 's|/etc|$RPM_BUILD_ROOT%{_sysconfdir}|' \
	-e 's|OPERA_SCRIPT_PATH=$0|OPERA_SCRIPT_PATH=|' install.sh

echo y |\
sh install.sh \
	--prefix=$RPM_BUILD_ROOT%{_prefix} \
	--wrapperdir=$RPM_BUILD_ROOT%{_bindir} \
	--docdir=$RPM_BUILD_ROOT%{_operadocdir} \
	--sharedir=$RPM_BUILD_ROOT%{_datadir}/opera \
	--exec_prefix=$RPM_BUILD_ROOT%{_libdir}/opera/bin \
	--plugindir=$RPM_BUILD_ROOT%{_plugindir}

# man install
install man/opera.1 $RPM_BUILD_ROOT%{_mandir}/man1

# wrapper correction
sed -i -e "s#$RPM_BUILD_ROOT##" $RPM_BUILD_ROOT%{_bindir}/opera

# install in kde etc.
install images/opera.xpm $RPM_BUILD_ROOT%{_pixmapsdir}

install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}

sed -i -e "s#$RPM_BUILD_ROOT##g" $RPM_BUILD_ROOT%{_datadir}/opera/java/*.policy

# always use latest possible wrapper
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/operamotifwrapper
if [ -f "$RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/operamotifwrapper-3" ]; then
	ln -sf operamotifwrapper-3 $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/operamotifwrapper-1
	ln -sf operamotifwrapper-3 $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/operamotifwrapper-2
elif [ -f "$RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/operamotifwrapper-2" ]; then
	ln -sf operamotifwrapper-2 $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/operamotifwrapper-1
	ln -sf operamotifwrapper-2 $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/operamotifwrapper-3
elif [ -f "$RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/operamotifwrapper-1" ]; then
	ln -sf operamotifwrapper-1 $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/operamotifwrapper-2
	ln -sf operamotifwrapper-1 $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/operamotifwrapper-3
fi

# clean unneeded files
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/config

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE
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
%{_pixmapsdir}/opera.xpm
%{_desktopdir}/*.desktop

%{_mandir}/man1/opera.1*

%config(noreplace) %verify(not md5 mtime size) /etc/opera*rc*
