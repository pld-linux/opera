#
# There're some problems with "shared" version
#
%define ver	6.11
%define	rel	20021129.1
Summary:	World fastest web browser
Summary(pl):	Najszybsza przegl±darka WWW na ¶wiecie
Name:		opera
Version:	%{ver}.%{rel}
Release:	2
License:	Restricted, see file LICENSE
Group:		X11/Applications/Networking
Source0:	ftp://ftp.task.gda.pl/pub/opera/linux/611/final/en/i386/static/%{name}-%{ver}-%{rel}-static-qt.i386.tar.gz
Source1:	ftp://ftp.task.gda.pl/pub/opera/linux/611/final/en/ppc/static/%{name}-%{ver}-%{rel}-static-qt.ppc.tar.gz
Source2:	http://web.opera.com/download/unix/locale/pl.qm.gz
Source3:	opera.desktop
NoSource:	0
URL:		http://www.opera.com/
ExclusiveArch:	%{ix86} ppc
Requires:	freetype >= 2
Requires:	openmotif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/opera/plugins
%define		_operadocdir	%{_docdir}/%{name}-%{ver}.%{rel}
%define		configfile	%{_datadir}/opera/config/opera6rc

%description
Opera is world fastest web browser. It supports most of nowaday
extensions of HTML. And it is quite stable. Only disadvantage are
advertisements on the top of its window. Version static linked with qt.

%description -l pl
Opera jest najszybsz± przegl±dark± WWW na ¶wiecie. Obs³uguje wiêkszo¶æ
dzisiejszych rozszerzeñ HTMLa. Dodatkowo jest w miarê stabilna. Jedyn±
niedogodno¶ci± s± reklamy ukazuj±ce siê w górze okna. Wersja statycznie
linkowana z qt.

%prep
%ifarch %{ix86}
%setup -q  -n %{name}-%{ver}-%{rel}-static-qt.i386
%endif
%ifarch ppc
%setup -q -T -b 1 -n %{name}-%{ver}-%{rel}-static-qt.ppc
%endif

%install
rm -rf $RPM_BUILD_ROOT

sh install.sh \
  --prefix=$RPM_BUILD_ROOT%{_prefix} \
  --wrapperdir=$RPM_BUILD_ROOT%{_bindir} \
  --docdir=$RPM_BUILD_ROOT%{_operadocdir} \
  --sharedir=$RPM_BUILD_ROOT%{_datadir}/opera \
  --exec_prefix=$RPM_BUILD_ROOT%{_datadir}/opera/bin \
  --plugindir=$RPM_BUILD_ROOT%{_plugindir}

# Polish locale
gunzip -c %{SOURCE2} > $RPM_BUILD_ROOT%{_datadir}/opera/locale/pl.qm

# man install
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install man/opera.1 $RPM_BUILD_ROOT%{_mandir}/man1

# wrapper correction
sed s#$RPM_BUILD_ROOT## > $RPM_BUILD_ROOT%{_bindir}/opera2 $RPM_BUILD_ROOT%{_bindir}/opera
mv $RPM_BUILD_ROOT%{_bindir}/opera2 $RPM_BUILD_ROOT%{_bindir}/opera

# install in kde etc.
install -d $RPM_BUILD_ROOT%{_pixmapsdir}
install images/opera.xpm $RPM_BUILD_ROOT%{_pixmapsdir}

install -d $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW
install %{SOURCE3} $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW

# symlink który niweluje burkanie siê opery :>
#ln -sf %{_datadir}/opera/ $RPM_BUILD_ROOT/usr/share/
#ln -sf %{_libdir}/opera $RPM_BUILD_ROOT/usr/lib/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE bugreport help
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/opera
%dir %{_datadir}/opera/bin
%attr(755,root,root) %{_datadir}/opera/bin/*
%{_datadir}/opera/buttons
%{_datadir}/opera/config
%{_datadir}/opera/help
%{_datadir}/opera/images
%{_datadir}/opera/java
%{_datadir}/opera/locale
%{_datadir}/opera/skin
%{_datadir}/opera/styles
%ifarch %{ix86}
%attr(755,root,root) %{_datadir}/opera/chartables.bin
%endif
%ifarch ppc
%attr(755,root,root) %{_datadir}/opera/chartables-be.bin
%endif
%attr(755,root,root) %{_datadir}/opera/opera6.adr
%dir %{_libdir}/opera
%dir %{_plugindir}
%attr(755,root,root) %{_plugindir}/*

%{_pixmapsdir}/opera.xpm
%{_applnkdir}/Network/WWW/*.desktop

%{_mandir}/man1/opera.1*
