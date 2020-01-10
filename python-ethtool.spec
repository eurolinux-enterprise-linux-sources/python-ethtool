%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_ver: %define python_ver %(%{__python} -c "import sys ; print sys.version[:3]")}

Summary: Ethernet settings python bindings
Name: python-ethtool
Version: 0.6
Release: 3%{?dist}
URL: http://fedorapeople.org/gitweb?p=dsommers/public_git/python-ethtool.git;a=summary
Source: http://dsommers.fedorapeople.org/python-ethtool/%{name}-%{version}.tar.bz2
Patch0: python-ethtool-0.3-doc.patch
Patch1: python-ethtool-aa2c20e697af1907b92129410aa10952a3ffdd68-fix-RETURN_NONE-refcount.patch
Patch2: python-ethtool-4e928d62a8e3c1dfefe6a55b81c0f0b4510b14eb-fix-error-handling.patch

# Cherrypick upstream fix for typo in the "pethtool --help" message
# (rhbz#692028):
Patch3: python-ethtool-710766dc72260149bd78fd6168fbaf6838fc3d4f-fix-typo-in-pethtool-help.patch

# Cherrypick upstream fix for memory leaks (rhbz#698125):
Patch4: python-ethtool-abc7f912f66d41dd734a10900429d4cad9377da5-fix-memory-leaks.patch

# Add IPv6 information to pifconfig (rhbz#698192):
Patch5: python-ethtool-0.6-add-ipv6-info-to-pifconfig.patch

# Cherrypick upstream fix for pifconfig's command-line parsing, to respect
# interface arguments (rhbz#714753)
Patch6: python-ethtool-a45819ecb5580aeeb09c6c2201929257f5d311d2-fix-pifconfig-command-line-parsing.patch

# Add a get_ipv4_addresses() method to ethtool.etherinfo to support devices
# with multiple IPv4 addresses (rhbz#759150):
Patch7: python-ethtool-0.6-add-get_ipv4_addresses-method.patch

License: GPLv2
Group: System Environment/Libraries
BuildRequires: python-devel libnl-devel asciidoc
BuildRequires: pkgconfig gcc
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Python bindings for the ethtool kernel interface, that allows querying and
changing of Ethernet card settings, such as speed, port, auto-negotiation, and
PCI locations.

%prep
%setup -q
%patch0 -p1 -b .doc
%patch1 -p1 -b .fix-RETURN_NONE-refcount
%patch2 -p1 -b .fix-error-handling

%patch3 -p1 
%patch4 -p1 -b .fix-memory-leaks
%patch5 -p1 
%patch6 -p1 
%patch7 -p1 -b .759150

%build
%{__python} setup.py build
a2x -d manpage -f manpage man/pethtool.8.asciidoc
a2x -d manpage -f manpage man/pifconfig.8.asciidoc
 
%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8
cp -p pethtool.py %{buildroot}%{_sbindir}/pethtool
cp -p pifconfig.py %{buildroot}%{_sbindir}/pifconfig
%{__gzip} -c man/pethtool.8 > %{buildroot}/%{_mandir}/man8/pethtool.8.gz
%{__gzip} -c man/pifconfig.8 > %{buildroot}/%{_mandir}/man8/pifconfig.8.gz

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING
%doc %{_mandir}/man8/*
%{_sbindir}/pethtool
%{_sbindir}/pifconfig
%{python_sitearch}/ethtool.so
%if "%{python_ver}" >= "2.5"
%{python_sitearch}/*.egg-info
%endif

%changelog
* Thu Dec 13 2012 David Malcolm <dmalcolm@redhat.com> - 0.6-3
- update python-ethtool-0.6-add-get_ipv4_addresses-method.patch, addressing
bug 886644, memory leaks, and a crasher when the broadcast address is NULL
Resolves: rhbz#886644

* Fri Oct 12 2012 David Malcolm <dmalcolm@redhat.com> - 0.6-2
- fix typo in pethtool --help
Resolves: rhbz#692028
- fix memory leaks
Resolves: rhbz#698125
- add IPv6 information to pifconfig
Resolves: rhbz#698192
- respect interface arguments to pifconfig
Resolves: rhbz#714753
- add a get_ipv4_addresses() method to ethtool.etherinfo to support devices
with multiple IPv4 addresses
Resolves: rhbz#759150

* Wed Mar  2 2011 David Malcolm <dmalcolm@redhat.com> - 0.6-1
- cherrypick fixes for Py_None reference leak, and for some error-handling bugs
Resolves: rhbz#680269

* Thu Feb 24 2011 David Sommerseth <davids@redhat.com> - 0.6-0
- Rebased to upstream python-ethtool-0.6

* Fri Feb  4 2011 Jeff Garzik <jgarzik@redhat.com> - 0.3-5.2
- Import man page patch from Fedora BZ# 638475
- Fix description spelling errors found by rpmlint.
- Fixes BZ# 605535

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.3-5.1
- Rebuilt for RHEL 6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.3-3
- Rebuild for Python 2.6

* Fri Sep  5 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.3-2
- Rewrote build and install sections as part of the fedora review process
  BZ #459549

* Tue Aug 26 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.3-1
- Add get_flags method from the first python-ethtool contributor, yay
- Add pifconfig command, that mimics the ifconfig tool using the
  bindings available

* Wed Aug 20 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.2-1
- Expand description and summary fields, as part of the fedora
  review process.

* Tue Jun 10 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.1-3
- add dist to the release tag

* Tue Dec 18 2007 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.1-2
- First build into MRG repo

* Tue Dec 18 2007 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.1-1
- Get ethtool code from rhpl 0.212
