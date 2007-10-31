# BRANCHES:
# - HEAD - stable version
# - DEVEL - development version
# - WEEKLY - weekly development version

# TODO:
# - move translations into a separate, noarch package
#
%bcond_without	shared		# static or shared version
%bcond_without	distributable	# distributable or not
%bcond_without	incall		# include all tarballs into src.rpm (but splitted into shared/static)

%define	ver		9.24
%define	sver		9.24
%define	fix		%{nil}
%define	dirrel		20071015
%define	reltype		final
%define	magicstr	671

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
		%define	rel		%{sparc_shared_rel}
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
%define	need_ix86_shared	0
%define	need_sparc_shared	0
%define	need_ppc_shared		0
%define	need_ix86_static	0
%define	need_sparc_static	0
%define	need_ppc_static		0

%if %{with incall}
	%if %{with shared}
		%define	need_ix86_shared	1
		%define	need_sparc_shared	1
		%define	need_ppc_shared	1
	%else
		%define	need_ix86_static	1
		%define	need_sparc_static	1
		%define	need_ppc_static	1
	%endif
%else
	%ifnarch %{ix86}
		%ifarch	sparc sparc64
			%if	%{with shared}
				%define	need_sparc_shared	1
			%else
				%define	need_sparc_static	1
			%endif
		%else
			%ifarch	ppc
				%if	%{with shared}
					%define	need_ppc_shared	1
				%else
					%define	need_ppc_static	1
				%endif
			%endif
		%endif
	%endif
%endif

%define		_rel	2
Summary:	World fastest web browser
Summary(pl.UTF-8):	Najszybsza przeglądarka WWW na świecie
Name:		opera
Version:	%{ver}%{fix}
Release:	%{_rel}
Epoch:		2
License:	Distributable
Group:		X11/Applications/Networking

%if %{need_ix86_static}
Source0:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/i386/static/%{name}-%{sver}-%{x86_static_rel}-static-qt.i386-en.tar.bz2
# Source0-md5:	96b8010ddb0ff250817c7fb314de2d26
%{!?with_distributable:NoSource:	0}
%endif

%if %{need_sparc_static}
Source1:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/sparc/static/%{name}-%{sver}-%{sparc_static_rel}-static-qt.sparc-en.tar.bz2
# Source1-md5:	c8443b4b83b21a56fdd8dc3526eaf46f
%{!?with_distributable:NoSource:	1}
%endif

%if %{need_ppc_static}
Source2:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/ppc/static/%{name}-%{sver}-%{ppc_static_rel}-static-qt.ppc-en.tar.bz2
# Source2-md5:	be68f701224493bbd9a6d62df8eb9b19
%{!?with_distributable:NoSource:	2}
%endif

%if %{need_ix86_shared}
Source20:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/i386/shared/%{name}-%{sver}-%{x86_shared_rel}-shared-qt.i386-en.tar.bz2
# Source20-md5:	e7d934c0fe9ce0ef7cec67981b71332d
%{!?with_distributable:NoSource:	20}
%endif

%if %{need_sparc_shared}
Source21:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/sparc/shared/gcc-2.95/%{name}-%{sver}-%{sparc_shared_rel}-shared-qt.sparc-en.tar.bz2
# Source21-md5:	84df0097ac9c52e95bc74e73407386ee
%{!?with_distributable:NoSource:	21}
%endif


%if %{need_ppc_shared}
Source22:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/ppc/shared/gcc-2.95/%{name}-%{sver}-%{ppc_shared_rel}-shared-qt.ppc-en.tar.bz2
# Source22-md5:	07f97223ffcb2d2ab87c921ead880018
%{!?with_distributable:NoSource:	22}
%endif

Source4:	%{name}.desktop
Patch0:		%{name}-wrapper.patch
URL:		http://www.opera.com/
BuildRequires:	rpmbuild(macros) >= 1.356
BuildRequires:	sed >= 4.0
Requires:	browser-plugins >= 2.0
Requires:	freetype >= 2
Provides:	wwwbrowser
ExclusiveArch:	%{ix86} ppc sparc sparcv9
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
%setup -q -T -b %{?with_shared:2}0 -n %{name}-%{sver}-%{rel}-%{type}-qt.i386-en%{?magicstr:-%{magicstr}}
%endif
%ifarch sparc sparcv9
%setup -q -T -b %{?with_shared:2}1 -n %{name}-%{sver}-%{rel}-%{type}-qt.sparc-en-%{?magicstr:-%{magicstr}}
%endif
%ifarch ppc
%setup -q -T -b %{?with_shared:2}2 -n %{name}-%{sver}-%{rel}-%{type}-qt.ppc-en%{?magicstr:-%{magicstr}}
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

mv -f $RPM_BUILD_ROOT%{_datadir}/%{name}/config/* $RPM_BUILD_ROOT%{_sysconfdir}
install images/opera.xpm $RPM_BUILD_ROOT%{_pixmapsdir}

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
%attr(755,root,root) %{_plugindir}/*
%dir %{_datadir}/opera
%{_datadir}/opera/*.*
%{_datadir}/opera/ini
%{_datadir}/opera/java
%{_datadir}/opera/images
%{_datadir}/opera/skin
%{_datadir}/opera/styles
%dir %{_datadir}/opera/locale
%{_datadir}/opera/locale/en
%{_datadir}/opera/locale/english.lng
%{_desktopdir}/*.desktop
%{_mandir}/man1/opera.1*
%{_pixmapsdir}/opera.xpm
