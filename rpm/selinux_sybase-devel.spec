Name:		sybase-selinux-devel
Version:	%{_provided_version}
Release:	%{_provided_release}%{?dist}
Summary:	SELinux policy module for Sybase ASE - devel
License:	GPLv2
URL:		https://github.com/hubertqc/selinux_sybase
#Source:	%{name}-%{version}.tar.gz
BuildArch:	noarch

Requires:	selinux-policy-devel
Requires:	sybase-selinux = %{version}-%{release}

%description
SELinux policy development interface for Sybase policy module.

###################################

%clean
%{__rm} -rf %{buildroot}

#%prep
#%setup -q

###################################

%install

mkdir -p -m 0755 %{buildroot}/usr/share/selinux/devel/include/apps
install -m 0444 %{_builddir}/se_module/sybase.if %{buildroot}/usr/share/selinux/devel/include/apps/

###################################

%files
%defattr(-,root,root,-)

/usr/share/selinux/devel/include/apps/sybase.if