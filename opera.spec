%define 	subversion	b8-20010426.023

Summary:	World fastest web browser
Name:		opera
Version:	5.0
Release:	0
#Not sure about license
License:	GPL
Group:		X11/Applications/Networking
Group(de):	X11/Applikationen/Netzwerkwesen
Group(pl):	X11/Aplikacje/Sieciowe
Source0:	%{name}-%{version}-%{subversion}-dynamic.i386.tar.gz
Source1:	%{name}.sh
URL:		http://www.opera.com/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
Opera is world fastest web browser. It supports most of nowaday
extensions of HTML. And it is quite stable. Only disadvantage are
advertisements on the top of its window.

%prep
%setup -q -n %{name}-%{version}-%{subversion}-dynamic.i386

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_prefix}/bin
install -d $RPM_BUILD_ROOT%{_prefix}/share
install -d $RPM_BUILD_ROOT%{_prefix}/opera
install -d $RPM_BUILD_ROOT%{_prefix}/opera/{buttons,help,images,styles}

for i in buttons help images styles;
do cp -r $i $RPM_BUILD_ROOT%{_prefix}/share/opera;
done

cp opera.adr $RPM_BUILD_ROOT%{_prefix}/share/opera
cp opera $RPM_BUILD_ROOT%{_prefix}/bin/opera-bin
cp %{SOURCE1} $RPM_BUILD_ROOT%{_prefix}/bin/opera

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE
%attr(755,root,root) %{_prefix}/bin/*
%{_prefix}/share/opera
