Name:          bolt
Version:       0.9.1
Release:       2
Summary:       Userspace system daemon to enable security levels for Thunderbolt 3 on GNU/Linux.
License:       LGPLv2+
URL:           https://gitlab.freedesktop.org/bolt/bolt
Source0:       %{url}/-/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:        fix-avoid-multiple-g_log_set_writer_func-calls.patch

BuildRequires: gcc asciidoc meson libudev-devel  polkit-devel systemd
BuildRequires: pkgconfig(gio-2.0) pkgconfig(libudev) pkgconfig(systemd)

Requires(post): systemd 
Requires(preun): systemd 
Requires(postun): systemd 

%description
bolt is a system daemon to manage thunderbolt 3 devices via a D-BUS API.
Devices connected via Thunderbolt can be DMA masters and thus read
system memory without interference of the operating system (or even
the CPU). Version 3 of the interface provides 5 different security
levels(none, dponly, user, secure, usbonly), in order to mitigate
the aforementioned security risk that connected devices pose to the system. 
The security level is set by the system firmware.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
%meson -Ddb-name=boltd
%meson_build

%check
%meson_test

%install
%meson_install

%post
%systemd_post bolt.service

%preun
%systemd_preun bolt.service

%postun
%systemd_postun_with_restart bolt.service

%files
%license COPYING
%doc README.md
%{_bindir}/boltctl
%{_datadir}/dbus-1/interfaces/org.freedesktop.bolt.xml
%{_datadir}/polkit-1/actions/org.freedesktop.bolt.policy
%{_datadir}/polkit-1/rules.d/org.freedesktop.bolt.rules
%{_datadir}/dbus-1/system-services/org.freedesktop.bolt.service
%{_libexecdir}/boltd
%{_unitdir}/bolt.service
%{_udevrulesdir}/*-bolt.rules
%{_datadir}/dbus-1/system.d/org.freedesktop.bolt.conf
%ghost %dir %{_localstatedir}/lib/boltd

%files help
%{_mandir}/man1/boltctl.1*
%{_mandir}/man8/boltd.8*

%changelog
* Wed Feb 08 2023 wulei <wulei80@h-partners.com> - 0.9.1-2
- Fix avoid multiple g_log_set_writer_func calls

* Thu Jul 8 2021 xuguangmin <xuguangmin@kylinos.cn> - 0.9.1-1
- update to 0.9.1 

* Thu Nov 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 0.5-2
- Package init
