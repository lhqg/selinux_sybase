Name:		sybase-selinux
Version:	%{_provided_version}
Release:	%{_provided_release}%{?dist}
Summary:	SELinux policy module for Sybase ASE
License:	GPLv3
URL:		https://github.com/lhqg/selinux_sybase
#Source:	%{name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	selinux-policy-devel
BuildRequires:	make

Requires:	selinux-policy-targeted %{?_sepol_minver_cond}
Requires:	selinux-policy-targeted %{?_sepol_maxver_cond}

Requires:	policycoreutils
Requires:	policycoreutils-python-utils
Requires:	libselinux-utils

%description
SELinux policy module to confine Sybase ASE started using systemd.
Eeach systemd unit name must start with 'sybase', the Sybase ASE server
binary assigned the sybase_exec_t SELinux type.
The Sybase ASE will run in the sybase_t domain.

###################################

%clean
%{__rm} -rf %{buildroot}

#%prep
#%setup -q

###################################

%build

make -f /usr/share/selinux/devel/Makefile -C %{_builddir} sybase.pp

###################################

%install

mkdir -p -m 0755 %{buildroot}/usr/share/selinux/packages/targeted
mkdir -p -m 0755 %{buildroot}/%{_docdir}/%{name}
mkdir -p -m 0755 %{buildroot}/%{_datarootdir}/%{name}

install -m 0555 %{_builddir}/scripts/* %{buildroot}/%{_datarootdir}/%{name}/
install -m 0444 %{_builddir}/sybase.pp %{buildroot}/usr/share/selinux/packages/targeted/
install -m 0444 %{_builddir}/{LICENSE,README.md} %{buildroot}/%{_docdir}/%{name}/

###################################

%post

semodule -i /usr/share/selinux/packages/targeted/sybase.pp

if selinuxenabled
then
  semanage fcontext -l | grep -q '^/var/opt/sybase =' || semanage fcontext -a -e /var/lib/sybase /var/opt/sybase
  restorecon -RFi /{opt,srv,home,dev}/sybase 
  restorecon -RFi /{lib,etc}/systemd/system/sybase*
  restorecon -RFi /var/{lib,log,run,opt,tmp}/sybase

  restorecon -Fi /usr/share/selinux/packages/targeted/sybase.pp
fi

###################################

%postun

if [ $1 -eq 0 ]
then
  semodule -r sybase
fi

###################################

%files
%defattr(-,root,root,-)

/usr/share/selinux/packages/targeted/sybase.pp

%dir	%{_datarootdir}/%{name}
%{_datarootdir}/%{name}/*

%dir		%{_docdir}/%{name}
%license 	%{_docdir}/%{name}/LICENSE
%doc		%{_docdir}/%{name}/README.md
