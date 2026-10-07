Name:           lsi-hba-temp
Version:        1.0.0
Release:        1%{?dist}
Summary:        LSI HBA Temperature Monitoring Utility

License:        GPLv3
URL:            https://github.com/the-art-of-server/lsi-hba-temp
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
Requires:       bash, pciutils, gawk, util-linux, systemd

%description
A lightweight, robust hardware monitoring utility that polls and evaluates 
real-time temperatures for Broadcom / LSI storage controllers (HBAs). Supports 
ad-hoc queries, interactive intervals, and native systemd or standalone 
background POSIX daemons.

%prep
%setup -q -n lsi-hba-temp

%install
rm -rf %{buildroot}
install -d -m 0755 %{buildroot}%{_bindir}
install -d -m 0755 %{buildroot}%{_sysconfdir}
install -d -m 0755 %{buildroot}%{_unitdir}

# Install script, config file, and systemd units
install -m 0755 lsi-hba-temp %{buildroot}%{_bindir}/lsi-hba-temp
install -m 0644 lsi-hba-temp.conf %{buildroot}%{_sysconfdir}/lsi-hba-temp.conf
install -m 0644 systemd/lsi-hba-temp.service %{buildroot}%{_unitdir}/lsi-hba-temp.service

%post
%systemd_post lsi-hba-temp.service

%preun
%systemd_preun lsi-hba-temp.service

%postun
%systemd_postun_with_restart lsi-hba-temp.service

%files
%license LICENSE
%doc README.md README_Unraid.txt README_TrueNAS.txt
%{_bindir}/lsi-hba-temp
%config(noreplace) %{_sysconfdir}/lsi-hba-temp.conf
%{_unitdir}/lsi-hba-temp.service

%changelog
* Wed Jul  8 2026 The Art of Server <the.art.of.server@gmail.com> - 1.0.0-1
- Initial public release packaging.
