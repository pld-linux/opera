#
# There're some problems with "shared" version
#
%bcond_with	shared

%define	ver		7.51
%define shver		%(echo %{ver} | tr -d .)
%define	dirrel		20040602
# is this snap or beta/final release?
%define	notsnap		1
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
%ifarch %{ix86}
%define	rel		%{x86_shared_rel}
%endif
%ifarch sparc64 sparc
%define	rel		%{sparc_shared_rel}
%endif
%ifarch ppc
%define	rel		%{ppc_shared_rel}
%endif
%else
%define	type		static
%ifarch %{ix86}
%define	rel		%{x86_static_rel}
%endif
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
Release:	1
License:	Restricted, see file LICENSE
Group:		X11/Applications/Networking
%if %{without shared}
%ifarch %{ix86}
%if %{notsnap}
Source0:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/i386/static/%{name}-%{ver}-%{x86_static_rel}-static-qt.i386-en.tar.bz2
%else
Source0:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/intel-linux/en/%{name}-%{ver}-%{x86_static_rel}-static-qt.i386-en.tar.bz2
%endif
NoSource:	0
%endif
%ifarch sparc64 sparc
%if %{notsnap}
Source1:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/sparc/static/%{name}-%{ver}-%{sparc_static_rel}-static-qt.sparc-en.tar.bz2
%else
Source1:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/sparc-linux/en/%{name}-%{ver}-%{sparc_static_rel}-static-qt.sparc-en.tar.bz2
%endif
NoSource:	1
%endif
%ifarch ppc
%if %{notsnap}
Source2:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/ppc/static/%{name}-%{ver}-%{ppc_static_rel}-static-qt.ppc-en.tar.bz2
%else
Source2:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/ppc-linux/en/%{name}-%{ver}-%{ppc_static_rel}-static-qt.ppc-en.tar.bz2
%endif
NoSource:	2
%endif
%else
%ifarch %{ix86}
%if %{notsnap}
Source20:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/i386/shared/%{name}-%{ver}-%{x86_shared_rel}-shared-qt.i386-en.tar.bz2
%else
Source20:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/intel-linux/en/%{name}-%{ver}-%{x86_shared_rel}-shared-qt.i386-en.tar.bz2
%endif
NoSource:	20
%endif
%ifarch sparc sparc64
%if %{notsnap}
Source21:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/sparc/shared/gcc-2.95/%{name}-%{ver}-%{sparc_shared_rel}-shared-qt.sparc-en.tar.bz2
%else
Source21:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/sparc-linux/en/%{name}-%{ver}-%{sparc_shared_rel}-shared-qt.sparc-en.tar.bz2
%endif
NoSource:	21
%endif
%ifarch ppc
%if %{notsnap}
Source22:	ftp://ftp.opera.com/pub/opera/linux/%{shver}/%{reltype}/en/ppc/shared/gcc-2.95/%{name}-%{ver}-%{ppc_shared_rel}-shared-qt.ppc-en.tar.bz2
%else
Source22:	http://snapshot.opera.com/unix/%{ver}-%{reltype}/ppc-linux/en/%{name}-%{ver}-%{ppc_shared_rel}-shared-qt.ppc-en.tar.bz2
%endif
NoSource:	22
%endif
%endif
Source3:	ftp://ftp.opera.com/pub/opera/unix/lng/721/pl/ou721_480pl.lng
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
%setup -q %{?with_shared:-T -b 20} -n %{name}-%{ver}-%{rel}-%{type}-qt.i386-en
%endif
%ifarch sparc sparc64
%setup -q -T -b %{?with_shared:2}1 -n %{name}-%{ver}-%{rel}-%{type}-qt.sparc-en
%endif
%ifarch ppc
%setup -q -T -b %{?with_shared:2}2 -n %{name}-%{ver}-%{rel}-%{type}-qt.ppc-en
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
install %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/opera/locale/polish.lng

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
ln -sf operamotifwrapper-3 $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/operamotifwrapper

# %{_libdir} is not the best place for it but opera doesn't search for it in better
# places :/
install lib/spellcheck.so $RPM_BUILD_ROOT%{_libdir}

# so big hack that you shouldn't even ask
objdump -p $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/operamotifwrapper-3 2>&1 | grep -E -q "NEEDED.*libXm.so.3" && %{__perl} -pi -e 's#libXm.so.3#libXm.so.4#g' $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/operamotifwrapper-3

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
%{_datadir}/opera/locale
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
