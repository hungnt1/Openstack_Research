Summary: Daemon that responds to network cables being plugged in and out
Name: netplug
Version: 1.2.9.2
Release: 4%{?dist}
License: GPLv2
Group: System Environment/Base
URL: http://www.red-bean.com/~bos/
Source0: http://www.red-bean.com/~bos/netplug/netplug-%{version}.tar.bz2

#execshield patch for netplug <t8m@redhat.com>
Patch1: netplug-1.2.9.2-execshield.patch

#fix netplugd init script (#242919)
#fix init script to be LSB-compliant (#522888)
Patch2: netplug-1.2.9.1-init.patch

Patch3: netplug-1.2.9.2-man.patch

Requires: iproute >= 2.4.7
Conflicts: net-tools < 1.60-96
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service
BuildRequires: gettext

%description
Netplug is a daemon that manages network interfaces in response to
link-level events such as cables being plugged in and out.  When a
cable is plugged into an interface, the netplug daemon brings that
interface up.  When the cable is unplugged, the daemon brings that
interface back down.

This is extremely useful for systems such as laptops, which are
constantly being unplugged from one network and plugged into another,
and for moving systems in a machine room from one switch to another
without a need for manual intervention.

%prep
%setup -q
%patch1 -p1 -b .execshield
%patch2 -p1 -b .init
%patch3 -p1 -b .man

%build
CFLAGS="$RPM_OPT_FLAGS" make

%install
rm -rf %{buildroot}
make install prefix=%{buildroot} \
             initdir=%{buildroot}/%{_initrddir} \
             mandir=%{buildroot}/%{_mandir}

mkdir -p %{buildroot}/%{_mandir}/man5
ln -fs %{_mandir}/man8/netplugd.8.gz %{buildroot}/%{_mandir}/man5/netplug.5.gz
ln -fs %{_mandir}/man8/netplugd.8.gz %{buildroot}/%{_mandir}/man5/netplug.d.5.gz
ln -fs %{_mandir}/man8/netplugd.8.gz %{buildroot}/%{_mandir}/man5/netplugd.conf.5.gz

%clean
rm -rf %{buildroot}

%post
  /sbin/chkconfig --add netplugd
  exit 0

%preun
if [ "$1" = "0" ]; then
  /sbin/chkconfig --del netplugd || :
  /sbin/service netplugd stop &> /dev/null || :
fi
exit 0

%postun
  /sbin/service netplugd condrestart >/dev/null 2>&1 || :
  exit 0

%files
%defattr(-,root,root)
%doc COPYING README TODO
/sbin/netplugd
%{_mandir}/man[58]/*
%{_sysconfdir}/netplug.d
%config(noreplace) %{_sysconfdir}/netplug.d/netplugd.conf
%{_initddir}/netplugd

%changelog
* Thu Apr 10 2014 Jiri Popelka <jpopelka@redhat.com> - 1.2.9.2-4
- revert systemd related changes to comply with el6

* Sun Aug 04 2013 Jiri Popelka <jpopelka@redhat.com> - 1.2.9.2-3
- BuildRequires: systemd due to  %%{_unitdir}

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Jiri Popelka <jpopelka@redhat.com> - 1.2.9.2-1
- provide native systemd unit file (#914762)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 30 2009  Jiri Popelka <jpopelka@redhat.com> - 1.2.9.1-3
- use %{_initddir} macro instead of deprecated %{_initrddir}

* Wed Sep 30 2009  Jiri Popelka <jpopelka@redhat.com> - 1.2.9.1-2
- fix init script to be LSB-compliant (#522888)

* Tue Sep 8 2009  Jiri Popelka <jpopelka@redhat.com> - 1.2.9.1-1
- Initial standalone package. Up to now netplug has been part of net-tools.

