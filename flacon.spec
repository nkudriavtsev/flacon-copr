Name:          flacon
Version:       3.1.1
Release:       3%{?dist}
Summary:       Audio File Encoder

License:       LGPLv2+
URL:           https://flacon.github.io/
Source0:       https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz
Source1:       %{name}.appdata.xml

BuildRequires: desktop-file-utils
BuildRequires: cmake
BuildRequires: libappstream-glib
BuildRequires: qt5-linguist
BuildRequires: qt5-qtbase-devel
BuildRequires: uchardet-devel

Requires: flac
Requires: opus-tools
Requires: vorbisgain
Requires: vorbis-tools
Requires: wavpack
Requires: lame


%description
Flacon extracts individual tracks from one big audio file containing
the entire album of music and saves them as separate audio files. 
To do this, it uses information from the appropriate CUE file. 
Besides, Flacon makes it possible to conveniently revise or specify 
tags both for all tracks at once or for each tag separately.


%prep
%autosetup


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%cmake  \
    -DBUILD_TESTS=Yes \
    -DUSE_QT5=Yes \
    ..
popd
make %{?_smp_mflags} -C %{_target_platform}


%install
make install DESTDIR=%{buildroot} -C %{_target_platform}
mkdir -p %{buildroot}%{_datadir}/appdata 
cp -a %{SOURCE1} %{buildroot}%{_datadir}/appdata
%find_lang %{name} --with-qt


%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
pushd %{_target_platform}
    cd tests && ./flacon_test || :
popd


%post
update-desktop-database &> /dev/null ||
touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:


%postun
update-desktop-database &> /dev/null ||
if [ $1 -eq 0 ] ; then 
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :


%files 
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/%{name}.*
%{_mandir}/man1/%{name}.1.*


%changelog
* Tue Sep 12 2017 Than Ngo <than@redhat.com> - 3.1.1-3
- enable build on ppc64

* Mon Sep 11 2017 Ilya Gradina <ilya.gradina@gmail.com> - 3.1.1-2
- fix build on ppc64 

* Sat Aug 12 2017 Ilya Gradina <ilya.gradina@gmail.com> - 3.1.1-1
- update to 3.1.1

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 29 2017 Ilya Gradina <ilya.gradina@gmail.com> - 3.0.0-1
- update to 3.0.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 28 2016 Ilya Gradina <ilya.gradina@gmail.com> - 2.1.1-1
- update to 2.1.1

* Thu Nov 10 2016 Ilya Gradina <ilya.gradina@gmail.com> - 2.1.0-1
- update to 2.1.0

* Wed Aug 17 2016 Ilya Gradina <ilya.gradina@gmail.com> - 2.0.1-5
- changes in appdata file

* Tue May 10 2016 Ilya Gradina <ilya.gradina@gmail.com> - 2.0.1-4
- remove the requires libfishsound
- changes in the appdata.xml file

* Sat May  7 2016 Ilya Gradina <ilya.gradina@gmail.com> - 2.0.1-3
- added xml file

* Sat Apr 30 2016 Ilya Gradina <ilya.gradina@gmail.com> - 2.0.1-2
- changes in the file, thx Jiri Eischmann 1264715#c3

* Wed Apr 27 2016 Ilya Gradina <ilya.gradina@gmail.com> - 2.0.1-1
- update to 2.0.1 
- few small changes

* Mon Sep 21 2015 Ilya Gradina <ilya.gradina@gmail.com> - 1.2.0-1
- Initial package
