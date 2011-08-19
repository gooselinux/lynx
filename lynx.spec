Summary: A text-based Web browser
Name: lynx
Version: 2.8.6
Release: 27%{?dist}
License: GPLv2
Group: Applications/Internet
Source: http://lynx.isc.org/lynx%{version}/lynx%{version}.tar.bz2
URL: http://lynx.isc.org/
Patch0: lynx-2.8.6-redhat.patch
Patch1: lynx-crash.patch
Patch2: lynx-2.8.6-options.patch
Patch3: lynx-2.8.6-backgrcolor.patch
Patch4: lynx-2.8.6-fmt_string.patch
Patch5: lynx-build-fixes.patch
Patch6: lynx-more-build-fixes.patch
Patch7: lynx-CVE-2008-4690.patch
Patch8: lynx-2.8.7-bm-del.patch

#582544
Patch9: lynx-2.8.6-noterm-crash.patch

Requires: goose-indexhtml
Provides: webclient
Provides: text-www-browser
BuildRequires: gettext
BuildRequires: openssl-devel
BuildRequires: ncurses-devel
BuildRequires: rsh
BuildRequires: slang-devel
BuildRequires: telnet
BuildRequires: unzip
BuildRequires: zip
BuildRequires: zlib-devel
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Lynx is a text-based Web browser. Lynx does not display any images,
but it does support frames, tables, and most other HTML tags. One
advantage Lynx has over graphical browsers is speed; Lynx starts and
exits quickly and swiftly displays web pages.

%prep
%setup -q -n lynx2-8-6
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
perl -pi -e "s,^HELPFILE:.*,HELPFILE:file://localhost/usr/share/doc/lynx-%{version}/lynx_help/lynx_help_main.html,g" lynx.cfg
perl -pi -e "s,^DEFAULT_INDEX_FILE:.*,DEFAULT_INDEX_FILE:http://www.google.com/,g" lynx.cfg
perl -pi -e 's,^#LOCALE_CHARSET:.*,LOCALE_CHARSET:TRUE,' lynx.cfg

%build
export PATH=`pwd`:$PATH
cat >gcc <<EOF
#!/bin/sh
ARGS=""
while [ \$# != 0 ]; do
	if [ \$1 != "-I/usr/include" -a \$1 != "-I/usr/include/" ]; then
		ARGS="\$ARGS \$1"
	fi
	shift
done
exec /usr/bin/gcc \$ARGS
EOF
chmod 0755 gcc
CFLAGS="-ggdb $RPM_OPT_FLAGS -DNCURSES -DNCURSES_MOUSE_VERSION" ; export CFLAGS
CXXFLAGS="-ggdb $RPM_OPT_FLAGS -DNCURSES -DNCURSES_MOUSE_VERSION" ; export CXXFLAGS
if pkg-config openssl ; then
	CPPFLAGS=`pkg-config --cflags openssl` ; export CPPFLAGS
	LDFLAGS=`pkg-config --libs-only-L openssl` ; export LDFLAGS
fi
%configure --libdir=/etc \
	--with-screen=ncursesw --enable-warnings \
	--enable-default-colors --enable-externs \
	--enable-internal-links --enable-nsl-fork \
	--enable-persistent-cookies --enable-prettysrc \
	--disable-font-switch --enable-source-cache \
	--enable-kbd-layout --with-zlib \
	--enable-charset-choice --enable-file-upload \
	--enable-cgi-links --enable-read-eta \
	--enable-addrlist-page --enable-cjk \
	--enable-justify-elts --enable-scrollbar \
	--enable-libjs --enable-cgi-links --enable-nls \
	--enable-ipv6 \
	--enable-locale-charset \
	--enable-japanese-utf8 \
	--with-ssl=%{_libdir}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
chmod -x samples/mailto-form.pl
%makeinstall mandir=$RPM_BUILD_ROOT%{_mandir}/man1 libdir=$RPM_BUILD_ROOT/etc
# Install Lang dependent resources
mkdir -p $RPM_BUILD_ROOT/usr/share/locale/ja/LC_MESSAGES/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/applnk/Internet

cat >$RPM_BUILD_ROOT%{_sysconfdir}/lynx-site.cfg <<EOF
# Place any local lynx configuration options (proxies etc.) here.
EOF

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc docs README INSTALLATION samples
%doc test lynx.hlp lynx_help
%{_bindir}/lynx
%{_mandir}/*/*
%config %{_sysconfdir}/lynx.cfg
%config(noreplace) %{_sysconfdir}/lynx.lss
%config(noreplace,missingok) %{_sysconfdir}/lynx-site.cfg

%changelog
* Fri Aug 19 2011 Mike Adams <shalkie@gooseproject.org> - 2.8.6-27
- changed the indexhtml to goose-indexhtml

* Fri May 14 2010 Kamil Dudka <kdudka@redhat.com> - 2.8.6-27
- use more suitable starting site (#591553)

* Mon Apr 19 2010 Kamil Dudka <kdudka@redhat.com> - 2.8.6-26
- do not crash when there is no terminal (#582544)

* Wed Jan 13 2010 Kamil Dudka <kdudka@redhat.com> - 2.8.6-25
- make it possible to delete a bookmark when ~/lynx_bookmarks.html is writable
  by group

* Tue Jan 07 2010 Kamil Dudka <kdudka@redhat.com> - 2.8.6-24
- updated sources URL
- cleanup in BuildRequires
- rediffed patches with non-zero offset

* Mon Nov 23 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.8.6-23.1
- Rebuilt for RHEL 6

* Fri Nov  6 2009 Jiri Moskovcak <jmoskovc@redhat.com> - 2.8.6-23
- removed dependency on indexthml
- changed default homepage to start.fedoraproject.org

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.8.6-22
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 2.8.6-19
- rebuild with new openssl

* Fri Nov  7 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 2.8.6-18
- Fixed CVE-2008-4690 lynx: remote arbitrary command execution.
  via a crafted lynxcgi: URL (thoger)

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.6-17
- fix license tag

* Thu May 29 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 2.8.6-16
- updated to latest stable version 2.8.6rel5
- Resolves: #214205
- added build patches from Dennis Gilmore
- skipped 2 releases to correct the NVR path

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.8.6-13
- Autorebuild for GCC 4.3

* Wed Jan 30 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 2.8.6-12
- added telnet, rsh, zip and unzip to BuildRequires
- Resolves: #430508

* Tue Jan  8 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 2.8.6-11
- fixed crash when using formatting character '$' in translation
- Resolves: #426449

* Tue Dec 11 2007 Ivana Varekova <varekova@redhat.com> - 2.8.6-10
- add default-colors option, change default setting (#409211)

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 2.8.6-9
 - Rebuild for openssl bump

* Wed Dec  5 2007 Ivana Varekova <varekova@redhat.com> - 2.8.6-8
- rebuild 

* Fri Oct 12 2007 Ivana Varekova <varekova@redhat.com> - 2.8.6-7
- add provides:text-www-browser flag

* Tue Oct  2 2007 Ivana Varekova <varekova@redhat.com> - 2.8.6-6
- fix 311031 - fix argument parsing

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.8.6-5
- Rebuild for selinux ppc32 issue.

* Tue Jul 17 2007 Ivana Varekova <varekova@redhat.com> - 2.8.6-4
- remove default-colors option

* Fri Feb 23 2007 Ivana Varekova <varekova@redhat.com> - 2.8.6-3
- incorporate package review feedback (#226113)

* Wed Oct 25 2006 Ivana Varekova <varekova@redhat.com> - 2.8.6-2
- add japanese unicode support (#143787)

* Tue Oct 24 2006 Ivana Varekova <varekova@redhat.com> - 2.8.6-1
- update to 2.8.6

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.8.5-28.1
- rebuild

* Tue May 30 2006 Ivana Varekova <varekova@redhat.com> - 2.8.5-28
- add buildreq gettext (#193515)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.8.5-27.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.8.5-27.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Nov 13 2005 Tim Waugh <twaugh@redhat.com> 2.8.5-27
- Apply patch to fix CVE-2005-2929 (bug #172973).

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 2.8.5-26
- rebuilt against new openssl

* Wed Nov  9 2005 Tim Waugh <twaugh@redhat.com> 2.8.5-25
- Rebuild for new openssl.

* Mon Oct 17 2005 Tim Waugh <twaugh@redhat.com> 2.8.5-24
- Apply patch to fix CAN-2005-3120 (bug #170253).

* Tue Mar 29 2005 Tim Waugh <twaugh@redhat.com> 2.8.5-23
- Fixed fix for bug #90302 (bug #152146).

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 2.8.5-22
- Rebuild for new GCC.

* Thu Jan  6 2005 Tim Waugh <twaugh@redhat.com> 2.8.5-21
- Fixed <option> handling (bug #90302).

* Thu Dec 30 2004 Tim Waugh <twaugh@redhat.com> 2.8.5-20
- Added --enable-locale-charset compilation option, set LOCALE_CHARSET
  on in the config file and removed i18ncfg patch (bug #124849).

* Fri Nov 19 2004 Tim Waugh <twaugh@redhat.com> 2.8.5-19
- 2.8.5rel1.  Fixes bug #139783.

* Thu Jul  8 2004 Tim Waugh <twaugh@redhat.com> 2.8.5-18
- Removed perl dependencies (bug #127423).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 25 2004 Tim Waugh <twaugh@redhat.com> 2.8.5-16
- No longer need lynx-284-ipv6-salen.patch.
- No longer need lynx2-8-2-telnet.patch.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 2.8.5-15
- rebuilt

* Mon Dec  1 2003 Tim Waugh <twaugh@redhat.com> 2.8.5-14
- Updated to dev16, fixing bug #110196.
- No longer need crlf patch.
- Use shipped ja translations.
- Use %%find_lang.
- Default config file now sets UTF-8 (bug #110986).

* Fri Jun 06 2003 Adrian Havill <havill@redhat.com> 2.8.5-13
- use wide version of ncurses for UTF-8

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Waugh <twaugh@redhat.com> 2.8.5-10
- Fix CRLF issue.

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2.8.5-9
- rebuild

* Fri Dec 20 2002 Elliot Lee <sopwith@redhat.com> 2.8.5-8
- _smp_mflags

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com>
- use openssl pkg-config data, if available

* Wed Nov 20 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches

* Thu Aug 08 2002 Karsten Hopp <karsten@redhat.de>
- remove menu entry (#69457)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 13 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.5-3
- Fix build with current toolchain

* Thu Nov 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.5-2
- Update (dev5)

* Wed Oct 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.5-1
- Update (dev3)
- Use "display" as image viewer (#54184)

* Tue Jul 31 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.4-17
- 2.8.4 release - no need to ship prerelease code...

* Thu Jul 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.4-16
- update to 2.8.4p5 (bugfix release)

* Tue Jul 10 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.4-15
- Add site-cfg file (#43841)

* Sun Jun 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.4-14
- 2.8.4p2

* Thu Jun 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- support newer gettext version

* Thu May  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.4-12
- --with-display=ncurses, fixes #37481

* Wed May  2 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.4-11
- Add Czech/Slovak patches from milan.kerslager@spsselib.hiedu.cz (RFE#38334)

* Sun Apr 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- dev20
- Add ipv6 patches from Pekka Savola <pekkas@netcore.fi>:
  - enable ipv6, patch for missing sockaddr sa_len
  - buildrequires: slang-devel, zlib-devel
  (Bug #35644)

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Thu Jan  4 2001 Nalin Dahyabhai <nalin@redhat.com>
- Fix up more of the i18ncfg patch

* Wed Jan  3 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.8.4dev16
- Fix up the i18ncfg patch - segfaulting on startup is not exactly
  a nice feature.
- Mark locale related files as such
- Mark /etc/lynx.cfg.ja as %%lang(ja)
- Add BuildRequires

* Thu Dec 21 2000 Yukihiro Nakai <ynakai@redhat.com>
- Add -enable-nls --with-included-gettext
- Add i18ncfg patch
- Add Japanese resources

* Thu Oct  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update build URL
- Fix help (Bug #18394)
- Replace the "index page link" (pointing to a Mosaic site with thousands
  of dead links) with a link to Google

* Sat Sep 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add https:// support (#17554)
- Update to dev10

* Fri Aug  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add Swedish and German translations to desktop file, Bug 15322

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul 11 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.8.4.dev.4

* Mon Jul 10 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up location of standard page and help page in lynx.cfg (still
  pointed at /usr/doc instead of /usr/share/doc, Bug #13227)

* Thu Jun 8 2000 Tim Powers <timp@redhat.com>
- fixed man page lolcation to be FHS compliant
- use predefined RPM macros wherever possible
- use %%makeinstall
- cleaned up files list

* Wed Apr 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- 2.8.3rel.1

* Tue Mar 28 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.8.3dev23
- add URL header

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- wmconfig -> desktop

* Sat Feb 05 2000 Cristian Gafton <gafton@redhat.com>
- version 2.8.3dev18
- drop the RFC compliance patch - they seemed to have done theiir own
- pray that ported patches are okay

* Mon Jan 31 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add "passive mode ftp" option, activated by PASSIVE:TRUE in /etc/lynx.cfg
- turn on "PASSIVE:TRUE" by default
- deal with the fact that RPM compresses man pages.

* Sun Jan 16 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add "view with less" download option

* Wed Nov  3 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix compliance with RFCs describing FTP.
  We can now connect to wu-ftpd >= 2.6.0 based servers.

* Wed Aug 25 1999 Bill Nottingham <notting@redhat.com>
- fix path to help file.
- turn off font switching
- disable args to telnet.

* Tue Jun 15 1999 Bill Nottingham <notting@redhat.com>
- update to 2.8.2

* Mon Mar 29 1999 Bill Nottingham <notting@redhat.com>
- apply some update patches from the lynx folks
- set user's TEMP dir to their home dir to avoid /tmp races

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 10)

* Wed Feb 24 1999 Bill Nottingham <notting@redhat.com>
- return of wmconfig

* Mon Nov 30 1998 Bill Nottingham <notting@redhat.com>
- create cookie file 0600

* Fri Nov  6 1998 Bill Nottingham <notting@redhat.com>
- update to 2.8.1rel2

* Thu Oct 29 1998 Bill Nottingham <notting@redhat.com>
- build for Raw Hide (slang-1.2.2)

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- 2.8.1pre9
- strip binaries

* Mon Oct 05 1998 Cristian Gafton <gafton@redhat.com>
- updated to lynx2.8.1pre.7.tar.gz

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon May 04 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 2.8rel3
- fixed mailto: buffer overflow (used Alan's patch)

* Fri Mar 20 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.8
- added buildroot

* Tue Jan 13 1998 Erik Troan <ewt@redhat.com>
- updated to 2.7.2
- enabled lynxcgi

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from 2.6 to 2.7.1
- moved /usr/lib/lynx.cfg to /etc/lynx.cfg
- build with slang instead of ncurses
- made default startup file be file:/usr/doc/HTML/index.html

