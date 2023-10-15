Name:		sybase-systemd
Version:	%{_provided_version}
Release:	%{_provided_release}%{?dist}
Summary:	Sybase systemd units
License:	GPLv2
URL:		https://github.com/hubertqc/selinux_sybase
#Source:	%{name}-%{version}.tar.gz
BuildArch:	noarch

Requires:	systemd
Requires:	sybase-selinux = %{version}-%{release}

%description
Definitions of systemd units for Sybase ASE.

###################################

%clean
%{__rm} -rf %{buildroot}

#%prep
#%setup -q

###################################

%install

mkdir -p -m 0755 %{buildroot}/%{_docdir}/%{name}/examples
mkdir -p -m 0755 %{buildroot}/usr/lib/systemd/system

install -m 0444 %{_builddir}/systemd/sybase-dataserver@.service %{buildroot}/usr/lib/systemd/system/
install -m 0444 %{_builddir}/systemd/sybase-backupserver@.service %{buildroot}/usr/lib/systemd/system/
install -m 0444 %{_builddir}/systemd/sybase@.target %{buildroot}/usr/lib/systemd/system/
install -m 0444 %{_builddir}/systemd/sybase.target %{buildroot}/usr/lib/systemd/system/
install -m 0444 %{_builddir}/systemd/sybase-shutdown.target %{buildroot}/usr/lib/systemd/system/

install -m 0444 %{_builddir}/systemd/env.SAMPLE %{buildroot}/%{_docdir}/%{name}/examples/

###################################

%post

if selinuxenabled
then
  restorecon -RFi /{lib,etc}/systemd/system/sybase*
  restorecon -RFi %{_docdir}/%{name}/
fi

systemctl daemon-reload
systemctl enable sybase.target
  
###################################

%postun

systemctl daemon-reload

###################################

%files
%defattr(-,root,root,-)

/usr/lib/systemd/system/sybase-dataserver@.service
/usr/lib/systemd/system/sybase-backupserver@.service
/usr/lib/systemd/system/sybase@.target
/usr/lib/systemd/system/sybase.target
/usr/lib/systemd/system/sybase-shutdown.target
  
%dir		%{_docdir}/%{name}
%doc		%{_docdir}/%{name}/examples/env.SAMPLE

