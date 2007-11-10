# BRANCHES:
# - HEAD - stable version
# - DEVEL - development version
# - WEEKLY - weekly development version

# TODO:
# - move translations into a separate, noarch package
#
%bcond_without	shared		# static or shared version
%bcond_without	distributable	# distributable or not
%bcond_with	snap		# snap version
%bcond_with	weekly		# weekly snapshot version

%define	ver		9.50
%define	dirrel		20071109
%define	reltype		snapshot
%define	magicstr	1662

%define sver            %{ver}
%define	shver		%(echo %{ver} | tr -d .)
%define	sreltype	%(echo %{reltype} | tr - _)
%define	x86_shared_rel		%{dirrel}.6
%define	x86_static_rel		%{dirrel}.9
%define	sparc_shared_rel	%{dirrel}.2
%define	sparc_static_rel	%{dirrel}.1
%define	ppc_shared_rel		%{dirrel}.6
%define	ppc_static_rel		%{dirrel}.1
%define x86_64_shared_rel       %{dirrel}.2
%define x86_64_static_rel       %{dirrel}.1

%if %{with shared}

%define	type		shared

# Defined to be able to build src.rpm also on not supported archs
%define	rel		%{x86_shared_rel}

%ifarch sparc sparcv9
%define	rel		%{sparc_shared_rel}
%endif

%ifarch ppc
%define	rel		%{ppc_shared_rel}
%endif

%ifarch %{x8664}
%define rel		%{x86_64_shared_rel}
%endif

%else # [with shared]

%define	type		static

# Defined to be able to build src.rpm also on not supported archs
%define	rel		%{x86_static_rel}

%ifarch sparc sparcv9
%define	rel		%{sparc_static_rel}
%endif

%ifarch ppc
%define	rel		%{ppc_static_rel}
%endif

%ifarch %{x8664}
%define rel             %{x86_64_static_rel}
%endif

%endif # [with shared]

%define		_rel	1
Summary:	World fastest web browser
Summary(pl.UTF-8):	Najszybsza przeglądarka WWW na świecie
Name:		opera
Version:	%{ver}
Release:	0.%{rel}.%{_rel}.%{sreltype}
Epoch:		2
License:	Distributable
Group:		X11/Applications/Networking

Source0:	http://snapshot.opera.com/unix/%{sreltype}-%{magicstr}/intel-linux/%{name}-%{sver}-%{x86_shared_rel}-shared-qt.i386-%{magicstr}.tar.bz2
# Source0-md5:	dfa36cd6f04b0116a435c51b650ba807
%{!?with_distributable:NoSource:	0}

#Source1:	http://snapshot.opera.com/unix/%{sreltype}-%{magicstr}/sparc-linux/%{name}-%{sver}-%{sparc_shared_rel}-shared-qt.sparc-%{magicstr}.tar.bz2
## Source1-md5:	913ccb28106f9f5acd3d94c8dc71ae1
#%{!?with_distributable:NoSource:	1}

Source2:	http://snapshot.opera.com/unix/%{sreltype}-%{magicstr}/ppc-linux/%{name}-%{sver}-%{ppc_shared_rel}-shared-qt.ppc-%{magicstr}.tar.bz2
# Source2-md5:	b6769dcb2775fbf9a92d6bcb88b7b717
%{!?with_distributable:NoSource:	2}

Source3:     http://snapshot.opera.com/unix/%{sreltype}-%{magicstr}/x86_64-linux/%{name}-%{sver}-%{x86_64_shared_rel}-shared-qt.x86_64-%{magicstr}.tar.bz2
# Source3-md5:	2e89836c24c947882c36638cb05c9c09
%{!?with_distributable:NoSource:        3}

Source10:	http://snapshot.opera.com/unix/%{sreltype}-%{magicstr}/intel-linux/%{name}-%{sver}-%{x86_static_rel}-static-qt.i386-%{magicstr}.tar.bz2
# Source10-md5:	f3f5ef04baf505f5c349c4f5d46589d1
%{!?with_distributable:NoSource:	10}

#Source11:	http://snapshot.opera.com/unix/%{sreltype}-%{magicstr}/sparc-linux/%{name}-%{sver}-%{sparc_static_rel}-static-qt.sparc-%{magicstr}.tar.bz2
## Source11-md5:	e190021f5530de3f711006cd9f6bb339
#%{!?with_distributable:NoSource:	11}

#Source12:	http://snapshot.opera.com/unix/%{sreltype}-%{magicstr}/ppc-linux/%{name}-%{sver}-%{ppc_static_rel}-static-qt.ppc-%{magicstr}.tar.bz2
## Source12-md5:	bf611c65fdf3342221e48ef690ef13d3
#%{!?with_distributable:NoSource:	12}

#Source13:	http://snapshot.opera.com/unix/%{sreltype}-%{magicstr}/x86_64-linux/%{name}-%{sver}-%{x86_64_static_rel}-static-qt.x86_64-%{magicstr}.tar.bz2
## Source13-md5:	40b850632dbb729a0bb16a1c450d97e5
#%{!?with_distributable:NoSource:	13}

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
%setup -q -T -b %{!?with_shared:1}0 -n %{name}-%{sver}-%{rel}-%{type}-qt.i386%{?magicstr:-%{magicstr}}
%endif

%ifarch sparc sparcv9
%setup -q -T -b %{!?with_shared:1}1 -n %{name}-%{sver}-%{rel}-%{type}-qt.sparc%{?magicstr:-%{magicstr}}
%endif

%ifarch ppc
%setup -q -T -b %{!?with_shared:1}2 -n %{name}-%{sver}-%{rel}-%{type}-qt.ppc%{?magicstr:-%{magicstr}}
%endif

%ifarch %{x8664}
%setup -q -T -b %{!?with_shared:1}3 -n %{name}-%{sver}-%{rel}-%{type}-qt.x86_64-%{magicstr}
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
