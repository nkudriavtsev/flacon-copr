# Disable tests because some of the tools are not available in Fedora
%bcond_with tests

Name:          flacon
Version:       4.1.0
Release:       2%{?dist}
Summary:       Audio File Encoder

License:       LGPLv2+
URL:           https://flacon.github.io/
Source0:       https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:       %{name}.appdata.xml

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5Network)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  uchardet-devel
# For %%check
BuildRequires:  %{_bindir}/appstream-util
BuildRequires:  %{_bindir}/desktop-file-validate
%if %{with tests}
# Test deps
BuildRequires:  %{_bindir}/mac
BuildRequires:  %{_bindir}/flac
BuildRequires:  %{_bindir}/wavpack
BuildRequires:  %{_bindir}/ttaenc
%endif

# formats/aac.h (encoder)
Recommends:     %{_bindir}/faac
# formats/ape.h (decoder)
Recommends:     %{_bindir}/mac
# formats/flac.h (encoder, decoder)
Recommends:     %{_bindir}/flac
# formats/flac.h (gain)
Recommends:     %{_bindir}/metaflac
# formats/mp3.h (encoder)
Recommends:     %{_bindir}/lame
# formats/mp3.h (gain)
Recommends:     %{_bindir}/mp3gain
# formats/ogg.h (encoder)
Recommends:     %{_bindir}/oggenc
# formats/ogg.h (gain)
Recommends:     %{_bindir}/vorbisgain
# formats/opus.h (encoder)
Recommends:     %{_bindir}/opusenc
# formats/tta.h (decoder)
Recommends:     %{_bindir}/ttaenc
# formats/wv.h (encoder)
Recommends:     %{_bindir}/wavpack
# formats/wc.h (decoder)
Recommends:     %{_bindir}/wvunpack
# formats/wc.h (gain)
Recommends:     %{_bindir}/wvgain

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
%cmake .. -DBUILD_TESTS=%{?with_tests:Yes}%{!?with_tests:No}
popd
%make_build -C %{_target_platform}

%install
%make_install -C %{_target_platform}
mkdir -p %{buildroot}%{_datadir}/appdata 
cp -a %{SOURCE1} %{buildroot}%{_datadir}/appdata
%find_lang %{name} --with-qt

%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
%if %{with tests}
cd %{_target_platform}/tests && ./flacon_test
%endif

%files -f %{name}.lang
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/translations
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_mandir}/man1/%{name}.1*

%changelog
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 25 2018 Ilya Gradina <ilya.gradina@gmail.com> - 4.1.0-1
- Update to 4.1.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.0.0-1.1
- Remove obsolete scriptlets

* Sun Dec 24 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.0.0-1
- Update to 4.0.0

* Sun Oct 01 2017 Ilya Gradina <ilya.gradina@gmail.com> - 3.1.1-4
- rebuilt package

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
