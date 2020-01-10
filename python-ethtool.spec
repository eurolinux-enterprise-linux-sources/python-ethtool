%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_ver: %define python_ver %(%{__python} -c "import sys ; print sys.version[:3]")}

Summary: Ethernet settings python bindings
Name: python-ethtool
Version: 0.6
Release: 1%{?dist}
URL: http://fedorapeople.org/gitweb?p=dsommers/public_git/python-ethtool.git;a=summary
Source: http://dsommers.fedorapeople.org/python-ethtool/%{name}-%{version}.tar.bz2
Patch0: python-ethtool-0.3-doc.patch
Patch1: python-ethtool-aa2c20e697af1907b92129410aa10952a3ffdd68-fix-RETURN_NONE-refcount.patch
Patch2: python-ethtool-4e928d62a8e3c1dfefe6a55b81c0f0b4510b14eb-fix-error-handling.patch

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
