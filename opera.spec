# BRANCHES:
# - HEAD - stable version
# - DEVEL - development version
# - WEEKLY - weekly development version (sometimes it's on DEVEL)

%bcond_without	shared		# static or shared version
%bcond_without	distributable	# distributable or not
%bcond_with	snap		# snap version
%bcond_with	weekly		# weekly snapshot version

%define	ver		9.52
%define	reltype		snapshot
%define	magicstr	2084

%define sver            %{ver}
%define	shver		%(echo %{ver} | tr -d .)
%define	sreltype	%(echo %{reltype} | tr - _)

# http://my.opera.com/csant/blog/2007/09/06/which-is-which
# http://my.opera.com/csant/blog/2008/05/20/which-is-which-part-two
%define	x86_shared_rel		gcc4-shared-qt3
%define	x86_static_rel		gcc4-qt4
%define	sparc_shared_rel	unknown
%define	sparc_static_rel	unknown
%define	ppc_shared_rel		gcc4-shared-qt3
%define	ppc_static_rel		gcc295-static-qt3
%define x86_64_shared_rel       gcc4-shared-qt3
%define x86_64_static_rel       unknown

%if %{with shared}

%define	type		shared

# Defined to be able to build src.rpm also on not supported archs
%define	rawrel		%{x86_shared_rel}

%ifarch sparc sparcv9
%define	rawrel		%{sparc_shared_rel}
%endif

%ifarch ppc
%define	rawrel		%{ppc_shared_rel}
%endif

%ifarch %{x8664}
%define rawrel		%{x86_64_shared_rel}
%endif

%else # [with shared]

%define	type		static

# Defined to be able to build src.rpm also on not supported archs
%define	rawrel		%{x86_static_rel}

%ifarch sparc sparcv9
%define	rawrel		%{sparc_static_rel}
%endif

%ifarch ppc
%define	rawrel		%{ppc_static_rel}
%endif

%ifarch %{x8664}
%define rawrel             %{x86_64_static_rel}
%endif

%endif # [with shared]

%define	rel	%(echo %{rawrel} | tr - _)

%define		_rel	1
Summary:	World fastest web browser
Summary(pl.UTF-8):	Najszybsza przeglądarka WWW na świecie
Name:		opera
Version:	%{ver}
Release:	0.%{?magicstr:%{magicstr}.}%{rel}.%{_rel}.%{sreltype}
Epoch:		2
License:	Distributable
Group:		X11/Applications/Networking

Source0:	http://snapshot.opera.com/unix/%{sreltype}-%{magicstr}/intel-linux/%{name}-%{sver}-%{magicstr}.%{x86_shared_rel}.i386.tar.bz2
# Source0-md5:	72e164278e94ea65e0678072726eaba7
%{!?with_distributable:NoSource:	0}

#Source1:	http://snapshot.opera.com/unix/%{sreltype}-%{magicstr}/sparc-linux/%{name}-%{sver}-%{magicstr}.%{sparc_shared_rel}-shared-qt.sparc.tar.bz2
## Source1-md5:	913ccb28106f9f5acd3d94c8dc71ae1
#%{!?with_distributable:NoSource:	1}

#Source2:	http://snapshot.opera.com/unix/%{sreltype}-%{magicstr}/ppc-linux/%{name}-%{sver}-%{magicstr}.%{ppc_shared_rel}.ppc.tar.bz2
## Source2-md5:	d8e072e6aad39ea3432658f68a455bc3
#%{!?with_distributable:NoSource:	2}

Source3:	http://snapshot.opera.com/unix/%{sreltype}-%{magicstr}/x86_64-linux/%{name}-%{sver}-%{magicstr}.%{x86_64_shared_rel}.x86_64.tar.bz2
# Source3-md5:	becc03d91e5b6a450b301188dd4bf6e5
%{!?with_distributable:NoSource:        3}

Source10:	http://snapshot.opera.com/unix/%{sreltype}-%{magicstr}/intel-linux/%{name}-%{sver}-%{magicstr}.%{x86_static_rel}.i386.tar.bz2
# Source10-md5:	d77e471448a12e9b2893de4f9e3a241b
%{!?with_distributable:NoSource:	10}

#Source11:	http://snapshot.opera.com/unix/%{sreltype}-%{magicstr}/sparc-linux/%{name}-%{sver}-%{magicstr}.%{sparc_static_rel}.sparc.tar.bz2
## Source11-md5:	e190021f5530de3f711006cd9f6bb339
#%{!?with_distributable:NoSource:	11}

#Source12:	http://snapshot.opera.com/unix/%{sreltype}-%{magicstr}/ppc-linux/%{name}-%{sver}-%{magicstr}.%{ppc_static_rel}.ppc.tar.bz2
## Source12-md5:	59c2f6f710c2efabeac9e153fa934743
#%{!?with_distributable:NoSource:	12}

#Source13:	http://snapshot.opera.com/unix/%{sreltype}-%{magicstr}/x86_64-linux/%{name}-%{sver}-%{magicstr}.%{x86_64_static_rel}.x86_64.tar.bz2
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
Obsoletes:	opera-i18n
ExclusiveArch:	%{ix86} %{x8664} ppc sparc sparcv9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/opera/plugins
%define		_operadocdir	%{_docdir}/%{name}-%{ver}

%description
Opera is world fastest web browser. It supports most of nowaday
extensions of HTML. And it is quite stable. This version is
%{?with_shared:shared}%{!?with_shared:statically} linked with Qt.

%description -l pl.UTF-8
Opera jest najszybszą przeglądarką WWW na świecie. Obsługuje większość
dzisiejszych rozszerzeń HTML-a. Dodatkowo jest w miarę stabilna. Ta
wersja jest skonsolidowana
%{?with_shared:dynamicznie}%{!?with_shared:statycznie} z Qt.

%package plugin32
Summary:	Opera 32-bit plugins support
Summary(pl.UTF-8):	Obsługa 32-bitowych wtyczek Opery
Group:		X11/Applications/Networking
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description plugin32
Opera 32-bit plugins support.

%description plugin32 -l pl.UTF-8
Obsługa 32-bitowych wtyczek Opery.

%prep
%ifarch %{ix86}
%setup -q -T -b %{!?with_shared:1}0 -n %{name}-%{sver}-%{?magicstr:%{magicstr}.}%{rawrel}.i386
%endif

%ifarch sparc sparcv9
%setup -q -T -b %{!?with_shared:1}1 -n %{name}-%{sver}-%{?magicstr:%{magicstr}.}%{rawrel}.sparc
%endif

%ifarch ppc
%setup -q -T -b %{!?with_shared:1}2 -n %{name}-%{sver}-%{?magicstr:%{magicstr}.}%{rawrel}.ppc
%endif

%ifarch %{x8664}
%setup -q -T -b %{!?with_shared:1}3 -n %{name}-%{sver}-%{?magicstr:%{magicstr}.}%{rawrel}.x86_64
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
%ifarch %{x8664}
%exclude %{_libdir}/opera/bin/*-ia32-*
%endif
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
%lang(be) %{_datadir}/opera/locale/be
%lang(bg) %{_datadir}/opera/locale/bg
%lang(cs) %{_datadir}/opera/locale/cs
%lang(da) %{_datadir}/opera/locale/da
%lang(de) %{_datadir}/opera/locale/de
%lang(el) %{_datadir}/opera/locale/el
%lang(en_GB) %{_datadir}/opera/locale/en-GB
%lang(es_ES) %{_datadir}/opera/locale/es-ES
%lang(es_LA) %{_datadir}/opera/locale/es-LA
%lang(fi) %{_datadir}/opera/locale/fi
%lang(fr) %{_datadir}/opera/locale/fr
%lang(fr_CA) %{_datadir}/opera/locale/fr-CA
%lang(fy) %{_datadir}/opera/locale/fy
%lang(hi) %{_datadir}/opera/locale/hi
%lang(hr) %{_datadir}/opera/locale/hr
%lang(hu) %{_datadir}/opera/locale/hu
%lang(it) %{_datadir}/opera/locale/it
%lang(ja) %{_datadir}/opera/locale/ja
%lang(ka) %{_datadir}/opera/locale/ka
%lang(ko) %{_datadir}/opera/locale/ko
%lang(lt) %{_datadir}/opera/locale/lt
%lang(mk) %{_datadir}/opera/locale/mk
%lang(nb) %{_datadir}/opera/locale/nb
%lang(nl) %{_datadir}/opera/locale/nl
%lang(nn) %{_datadir}/opera/locale/nn
%lang(pl) %{_datadir}/opera/locale/pl
%lang(pt) %{_datadir}/opera/locale/pt
%lang(pt_BR) %{_datadir}/opera/locale/pt-BR
%lang(ru) %{_datadir}/opera/locale/ru
%lang(sv) %{_datadir}/opera/locale/sv
%lang(tr) %{_datadir}/opera/locale/tr
%lang(zh_CN) %{_datadir}/opera/locale/zh-cn
%lang(zh_TW) %{_datadir}/opera/locale/zh-tw
%{_desktopdir}/*.desktop
%{_mandir}/man1/opera.1*
%{_pixmapsdir}/opera.xpm

%ifarch %{x8664}
%files plugin32
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/opera/bin/*-ia32-*
%endif
