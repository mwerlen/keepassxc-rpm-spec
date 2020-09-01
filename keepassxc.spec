%undefine __cmake_in_source_build
# EPEL7 not possible because libgcrypt version is 1.5

Name:           keepassxc
Version:        2.6.1
Release:        1%{?dist}
Summary:        Cross-platform password manager
License:        Boost and BSD and CC0 and GPLv3 and LGPLv2 and LGPLv2+ and LGPLv3+ and Public Domain
URL:            http://www.keepassxc.org/
Source0:     	https://github.com/keepassxreboot/keepassxc/releases/download/%{version}/keepassxc-%{version}-src.tar.xz

BuildRequires:  cmake >= 3.1
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++ >= 4.7
BuildRequires:  qt5-qtbase-devel >= 5.2
BuildRequires:  qt5-qttools-devel >= 5.2
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qrencode-devel
BuildRequires:  libargon2-devel
BuildRequires:  libcurl-devel
BuildRequires:  libgcrypt-devel >= 1.7
BuildRequires:  libmicrohttpd-devel
BuildRequires:  libsodium-devel
BuildRequires:  libXi-devel
BuildRequires:  libXtst-devel
BuildRequires:  libyubikey-devel
BuildRequires:  qt5-qtx11extras-devel
# For quazip read https://bugzilla.redhat.com/show_bug.cgi?id=1754061#c1
%if 0%{?el8}
BuildRequires:  quazip-devel
%else
BuildRequires:  quazip-qt5-devel
%endif
BuildRequires:  ykpers-devel
BuildRequires:  zlib-devel
BuildRequires:  libappstream-glib
BuildRequires:  qt5-qtbase-private-devel
BuildRequires:  readline-devel
BuildRequires:  rubygem-asciidoctor

%description
KeePassXC is a community fork of KeePassX
KeePassXC is an application for people with extremely high demands on secure
personal data management.
KeePassXC saves many different information e.g. user names, passwords, urls,
attachemts and comments in one single database. For a better management
user-defined titles and icons can be specified for each single entry.
Furthermore the entries are sorted in groups, which are customizable as well.
The integrated search function allows to search in a single group or the
complete database.
KeePassXC offers a little utility for secure password generation. The password
generator is very customizable, fast and easy to use. Especially someone who
generates passwords frequently will appreciate this feature.
The complete database is always encrypted either with AES (alias Rijndael) or
Twofish encryption algorithm using a 256 bit key. Therefore the saved
information can be considered as quite safe.



%prep
%autosetup

%build
# This package fails to build with LTO due to undefined symbols.  LTO
# was disabled in OpenSuSE as well, but with no real explanation why
# beyond the undefined symbols.  It really shold be investigated further.
# Disable LTO
%define _lto_cflags %{nil}

%cmake \
    -DWITH_TESTS=OFF \
    -DWITH_XC_ALL=ON \
    -DWITH_XC_KEESHARE_SECURE=ON \
    -WITH_XC_UPDATECHECK=ON \
    -DCMAKE_BUILD_TYPE=Release
%cmake_build
 
%install
%cmake_install
 
desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    --delete-original \
    --add-mime-type application/x-keepassxc \
    %{buildroot}%{_datadir}/applications/org.%{name}.KeePassXC.desktop
 
# Associate KDB* files
cat > x-keepassxc.desktop << EOF
[Desktop Entry]
Comment=
Hidden=false
Icon=keepassxc.png
MimeType=application/x-keepassxc
Patterns=*.kdb;*.KDB;*.kdbx;*.KDBX*
Type=MimeType
EOF
install -D -m 644 -p x-keepassxc.desktop \
    %{buildroot}%{_datadir}/mimelnk/application/x-keepassxc.desktop

#install appdata files

%find_lang keepassx --with-qt

%check
%ctest
desktop-file-validate %{buildroot}%{_datadir}/applications/org.%{name}.KeePassXC.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/org.%{name}.KeePassXC.appdata.xml

%files
%doc README.md
%license COPYING LICENSE*
%{_bindir}/keepassxc
%{_bindir}/keepassxc-cli
%{_bindir}/keepassxc-proxy
%{_datadir}/keepassxc
%{_datadir}/applications/org.%{name}.KeePassXC.desktop
%{_datadir}/metainfo/org.%{name}.KeePassXC.appdata.xml
%{_datadir}/mimelnk
%{_datadir}/mime/packages/*.xml
%{_datadir}/icons/hicolor/*/*/*keepassxc*
%{_libdir}/%{name}
%{_mandir}/man1/%{name}-cli.1*
%{_mandir}/man1/%{name}.1*

%changelog
* Thu Sep 01 2020 Maxime Werlen <maxime@werlen.fr> - 2.6.1-1
- Update to 2.6.1
- Apply commit bebd78 from Fedora repo by ignatenkobrain

* Wed Jul 15 2020 Maxime Werlen <maxime@werlen.fr> - 2.6.0-1
- Update to 2.6.0

* Tue Apr 14 2020 Maxime Werlen <maxime@werlen.fr> - 2.5.4-1
- Update to 2.5.4

* Mon Jan 20 2020 Maxime Werlen <maxime@werlen.fr> - 2.5.3-1
- Update to 2.5.3

* Mon Jan 13 2020 Maxime Werlen <maxime@werlen.fr> - 2.5.2-1
- Update to 2.5.2

* Tue Nov 12 2019 Maxime Werlen <maxime@werlen.fr> - 2.5.1-1
- Update to 2.5.1
- Added -DWITH_XC_KEESHARE_SECURE=ON from fedora - Germano Massullo <germano.massullo@gmail.com> - 2.4.3-4
- Added BuildRequires: quazip-devel from fedora - Germano Massullo <germano.massullo@gmail.com> - 2.4.3-6

* Wed Jul 17 2019 Maxime Werlen <maxime@werlen.fr> - 2.4.3-3
- Enable update check

* Tue Jun 25 2019 Bjรถrn Esser <besser82@fedoraproject.org> - 2.4.3-2
- Rebuilt (libqrencode.so.4)

* Tue Jun 11 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.4.3-1
- Update to 2.4.3

* Fri May 31 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2

* Tue Apr 16 2019 Germano Massullo <germano.massullo@gmail.com> - 2.4.1-1
- 2.4.1 release
- Added WITH_XC_UPDATECHECK=OFF

* Wed Mar 20 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0
- Drop unneeded sed lines in spec file
- Added BR for qrencode-devel and qt5-qtsvg-devel

* Mon Mar 18 2019 Remi Collet <remi@fedoraproject.org> - 2.3.4-3
- rebuild for libargon2 new soname

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 29 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.3.4-1
- Update to 2.3.4

* Thu Jul 19 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.3.3-3
- Fix FTBFS

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 10 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.3.3-1
- Update to 2.3.3

* Tue May 08 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2

* Wed Mar 07 2018 Germano Massullo <germano.massullo@gmail.com> - 2.3.1-1
- 2.3.1 release
- used -DWITH_XC_ALL=ON to enable all features. Read https://github.com/keepassxreboot/keepassxc/issues/1558#issuecomment-369291706

* Wed Feb 28 2018 Germano Massullo <germano.massullo@gmail.com> - 2.2.4-7
- added BuildRequires: libargon2-devel
- added BuildRequires: libcurl-devel
- added BuildRequires: libgcrypt-devel >= 1.7
- added BuildRequires: libsodium-devel
- added BuildRequires: gcc-c++ >= 4.7
- added %%{_mandir}/man1/%{name}-cli.1*

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.2.4-6
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.2.4-4
- Remove obsolete scriptlets

* Wed Dec 27 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.2.4-3
- Fix specfile error

* Sat Dec 16 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.2.4-2
- Adjust for changes in appdata and desktop filename change

* Thu Dec 14 2017 Germano Massullo <germano.massullo@gmail.com> - 2.2.4-1
- 2.2.4 release
- removed patch to fix typo in a XML tag

* Tue Dec 12 2017 Germano Massullo <germano.massullo@gmail.com> - 2.2.3-1
- 2.2.3 release
- added patch to fix typo in a XML tag

* Sun Oct 22 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2
- Fix desktop file names
- Added BR on libappstream-glib
- Install appdata file

* Mon Oct 02 2017 Germano Massullo <germano.massullo@gmail.com> - 2.2.1-1
- 2.2.1 release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Germano Massullo <germano.massullo@gmail.com> - 2.2.0-1
- 2.2.0 release
- added %%{_bindir}/keepassxc-cli
- changed -DWITH_XC_YUBIKEY=OFF to -DWITH_XC_YUBIKEY=ON
- added BuildRequires: ykpers-devel and BuildRequires: libyubikey-devel

* Fri May 19 2017 Germano Massullo <germano.massullo@gmail.com> - 2.1.4-2
- Disabled Yubikey support. It will be re-enabled on 2.2.0 release

* Sun May 14 2017 Germano Massullo <germano.massullo@gmail.com> - 2.1.4-1
- First release on Fedora repository

