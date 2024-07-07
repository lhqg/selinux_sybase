Name:		sybase-systemd
Version:	%{_provided_version}
Release:	%{_provided_release}%{?dist}
Summary:	Sybase systemd units
License:	GPLv3
URL:		https://github.com/lhqg/selinux_sybase
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
mkdir -p -m 0755 %{buildroot}/usr/share/%{name}
mkdir -p -m 0755 %{buildroot}/usr/lib/systemd/system
mkdir -p -m 0755 %{buildroot}/etc/udev/rules.d

install -m 0444 %{_builddir}/systemd/sybase-env@.service %{buildroot}/usr/lib/systemd/system/
install -m 0444 %{_builddir}/systemd/sybase-dataserver@.service %{buildroot}/usr/lib/systemd/system/
install -m 0444 %{_builddir}/systemd/sybase-backupserver@.service %{buildroot}/usr/lib/systemd/system/
install -m 0444 %{_builddir}/systemd/sybase@.target %{buildroot}/usr/lib/systemd/system/
install -m 0444 %{_builddir}/systemd/sybase.target %{buildroot}/usr/lib/systemd/system/
install -m 0444 %{_builddir}/systemd/sybase-shutdown.target %{buildroot}/usr/lib/systemd/system/

install -m 0444 %{_builddir}/systemd/env.SAMPLE %{buildroot}/%{_docdir}/%{name}/examples/
install -m 0555 %{_builddir}/systemd/mksetenv %{buildroot}/usr/share/%{name}/mksetenv

install -m 0444 %{_builddir}/udev.rules/99-sybase-rawdev.rules %{buildroot}//etc/udev/rules.d/

###################################

%post

if selinuxenabled
then
  restorecon -RFi /{lib,etc}/systemd/system/sybase*
  restorecon -RFi %{_docdir}/%{name}/
  restorecon -RFi /etc/udev/rules.d/
fi

systemctl daemon-reload
systemctl enable sybase.target
udevadm control --reload
  
###################################

%postun

systemctl daemon-reload
udevadm control --reload

###################################

%files
%defattr(-,root,root,-)

/usr/lib/systemd/system/sybase-env@.service
/usr/lib/systemd/system/sybase-dataserver@.service
/usr/lib/systemd/system/sybase-backupserver@.service
/usr/lib/systemd/system/sybase@.target
/usr/lib/systemd/system/sybase.target
/usr/lib/systemd/system/sybase-shutdown.target
/etc/udev/rules.d/99-sybase-rawdev.rules
  
%dir /usr/share/%{name}
/usr/share/%{name}/mksetenv

%dir		%{_docdir}/%{name}
%doc		%{_docdir}/%{name}/examples/env.SAMPLE

