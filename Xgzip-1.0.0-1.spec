Summary: Compresses and uncompresses files using accelerated/standard zlib
Name: Xgzip
Version: 1.0.0
Release: 1
License: Apache License 2.0
Group: Applications/File
Source0: https://github.com/aixoss/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: zlib-devel

%description
The Xgzip utility compress and decompress files. This Xgzip differs 
from the GNU gzip data compression program (gzip) in a way where the 
former uses zlib APIs to achieve the compression & decompression and 
the latter one uses it's own compression logic.
This software is mainly developed to exploit the hardware
accelerated zlib library but it can work with the general/standard 
zlib library as well.

%prep
%setup -q
rm -rf   /tmp/%{name}-%{version}-32bit
cp -pr . /tmp/%{name}-%{version}-32bit
rm -fr *
mv       /tmp/%{name}-%{version}-32bit 32bit
cp -pr 32bit 64bit


%build
PATH=/opt/freeware/bin:$PATH
export CC=/usr/vac/bin/xlc_r

#Build on 64bit mode
export OBJECT_MODE=64
cd 64bit
export CFLAGS=" -q64 -O2"
export LDFLAGS="-L/opt/zlibNX/lib -lz -L/usr/lib"
gmake

#Build on 32bit mode
export OBJECT_MODE=32
cd ../32bit
export CFLAGS=" -O2 -D_LARGE_FILES"
export LDFLAGS="-L/opt/zlibNX/lib -lz -L/usr/lib"
gmake


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

#Install on 64bit mode
export OBJECT_MODE=64
cd 64bit
make install DESTDIR=${RPM_BUILD_ROOT}

(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
    mv $fic "$fic"_64
    done
)

#Install on 32bit mode
export OBJECT_MODE=32
cd ../32bit
make install DESTDIR=${RPM_BUILD_ROOT}

/usr/bin/strip -X32_64 ${RPM_BUILD_ROOT}%{_bindir}/* || :

(
    cd  ${RPM_BUILD_ROOT}/%{_prefix}/bin
    for fic in $(ls -1| grep -v -e _32 -e _64)
    do
    mv $fic "$fic"_32
    ln -sf "$fic"_64 $fic
    done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,system)
%doc 32bit/LICENSE 32bit/README.md
%{_bindir}/*
%{_mandir}/man?/%{name}.*


%changelog
* Mon Jul 30 2018 Ayappan P <ayappap2@in.ibm.com> - 1.0.0-1
- First version 1.0.0
