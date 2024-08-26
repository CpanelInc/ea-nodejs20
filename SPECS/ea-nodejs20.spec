Name:    ea-nodejs20
Vendor:  cPanel, Inc.
Summary: Node.js 20
Version: 20.17.0
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: MIT
Group:   Development/Languages
URL:  https://nodejs.org
Source0: https://nodejs.org/dist/v%{version}/node-v%{version}-linux-x64.tar.gz

Provides: ea4-nodejs
Conflicts: ea4-nodejs
# Because old ea-nodejs10 does not have ^^^ and DNF wants to solve ^^^ by downgrading ea-nodejs10
Conflicts: ea-nodejs10

%description
Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine.

%prep
%setup -qn node-v%{version}-linux-x64

%build

# nodejs now has support for Microsoft Powershell, since that is not relevant
# to any of our deployed systems, I am removing them so they do not
# automatically require powershell, causing a dependency issue

cat > remove_pwsh.pl <<EOF
use strict;
use warnings;

my @files = split (/\n/, \`find . -type f -print\`);

foreach my \$file (@files) {
    my \$first_line = \`head -n 1 \$file\`;
    if (\$first_line =~ m/env\s+pwsh/) {
        print "Removing file \$file\n";
        unlink \$file;
    }
}
EOF

/usr/bin/perl remove_pwsh.pl

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs20
cp -r ./* $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs20

cd $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs20
for file in `find . -type f -print | xargs grep -l '^#![ \t]*/usr/bin/env node'`
do
    echo "Changing Shebang (env) for" $file
    sed -i '1s:^#![ \t]*/usr/bin/env node:#!/opt/cpanel/ea-nodejs20/bin/node:' $file
done

mkdir -p %{buildroot}/etc/cpanel/ea4
echo -n /opt/cpanel/ea-nodejs20/bin/node > %{buildroot}/etc/cpanel/ea4/passenger.nodejs

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
/opt/cpanel/ea-nodejs20
/etc/cpanel/ea4/passenger.nodejs
%attr(0755,root,root) /opt/cpanel/ea-nodejs20/bin/*


%changelog
* Wed Aug 21 2024 Cory McIntire <cory@cpanel.net> - 20.17.0-1
- EA-12348: Update ea-nodejs20 from v20.16.0 to v20.17.0

* Thu Aug 01 2024 Cory McIntire <cory@cpanel.net> - 20.16.0-1
- EA-12306: Update ea-nodejs20 from v20.15.1 to v20.16.0

* Tue Jul 09 2024 Cory McIntire <cory@cpanel.net> - 20.15.1-1
- EA-12264: Update ea-nodejs20 from v20.15.0 to v20.15.1
	- CVE-2024-36138 - Bypass incomplete fix of CVE-2024-27980 (High)
	- CVE-2024-22020 - Bypass network import restriction via data URL (Medium)
	- CVE-2024-22018 - fs.lstat bypasses permission model (Low)
	- CVE-2024-36137 - fs.fchown/fchmod bypasses permission model (Low)
	- CVE-2024-37372 - Permission model improperly processes UNC paths (Low)

* Mon Jul 01 2024 Cory McIntire <cory@cpanel.net> - 20.15.0-1
- EA-12240: Update ea-nodejs20 from v20.13.1 to v20.15.0

* Thu May 09 2024 Cory McIntire <cory@cpanel.net> - 20.13.1-1
- EA-12140: Update ea-nodejs20 from v20.13.0 to v20.13.1

* Tue May 07 2024 Cory McIntire <cory@cpanel.net> - 20.13.0-1
- EA-12128: Update ea-nodejs20 from v20.12.2 to v20.13.0

* Wed Apr 10 2024 Cory McIntire <cory@cpanel.net> - 20.12.2-1
- EA-12083: Update ea-nodejs20 from v20.12.1 to v20.12.2
- Command injection via args parameter of child_process.spawn without shell option enabled on Windows (CVE-2024-27980) - (HIGH)

* Wed Apr 03 2024 Cory McIntire <cory@cpanel.net> - 20.12.1-1
- EA-12068: Update ea-nodejs20 from v20.12.0 to v20.12.1
- CVE-2024-27983 - Assertion failed in node::http2::Http2Session::~Http2Session() leads to HTTP/2 server crash- (High)
- CVE-2024-27982 - HTTP Request Smuggling via Content Length Obfuscation - (Medium)

* Tue Mar 26 2024 Cory McIntire <cory@cpanel.net> - 20.12.0-1
- EA-12050: Update ea-nodejs20 from v20.11.1 to v20.12.0

* Wed Feb 14 2024 Cory McIntire <cory@cpanel.net> - 20.11.1-1
- EA-11975: Update ea-nodejs20 from v20.11.0 to v20.11.1
- CVE-2024-21892 - Code injection and privilege escalation through Linux capabilities- (High)
- CVE-2024-22019 - http: Reading unprocessed HTTP request with unbounded chunk extension allows DoS attacks- (High)
- CVE-2024-21896 - Path traversal by monkey-patching Buffer internals- (High)
- CVE-2024-22017 - setuid() does not drop all privileges due to io_uring - (High)
- CVE-2023-46809 - Node.js is vulnerable to the Marvin Attack (timing variant of the Bleichenbacher attack against PKCS#1 v1.5 padding) - (Medium)
- CVE-2024-21891 - Multiple permission model bypasses due to improper path traversal sequence sanitization - (Medium)
- CVE-2024-21890 - Improper handling of wildcards in --allow-fs-read and --allow-fs-write (Medium)
- CVE-2024-22025 - Denial of Service by resource exhaustion in fetch() brotli decoding - (Medium)

* Wed Jan 10 2024 Cory McIntire <cory@cpanel.net> - 20.11.0-1
- EA-11904: Update ea-nodejs20 from v20.10.0 to v20.11.0

* Wed Nov 29 2023 Cory McIntire <cory@cpanel.net> - 20.10.0-1
- EA-11826: Update ea-nodejs20 from v20.9.0 to v20.10.0

* Thu Oct 26 2023 Cory McIntire <cory@cpanel.net> - 20.9.0-1
- EA-11773: Update ea-nodejs20 from v20.8.1 to v20.9.0

* Mon Oct 16 2023 Cory McIntire <cory@cpanel.net> - 20.8.1-1
- EA-11747: Update ea-nodejs20 from v20.8.0 to v20.8.1

* Mon Oct 02 2023 Cory McIntire <cory@cpanel.net> - 20.8.0-1
- EA-11715: Update ea-nodejs20 from v20.7.0 to v20.8.0
    undici - Cookie headers are not cleared in cross-domain redirect in undici-fetch (High) - (CVE-2023-45143)
    nghttp2 - HTTP/2 Rapid Reset (High) - (CVE-2023-44487)
    Permission model improperly protects against path traversal (High) - (CVE-2023-39331)
    Path traversal through path stored in Uint8Array (High) - (CVE-2023-39332)
    Integrity checks according to policies can be circumvented (Medium) - (CVE-2023-38552)
    Code injection via WebAssembly export names (Low) - (CVE-2023-39333)

* Wed Sep 20 2023 Travis Holloway <t.holloway@cpanel.net> - 20.7.0-1
- EA-11698: Update ea-nodejs20 from v20.6.1 to v20.7.0

* Fri Sep 15 2023 Cory McIntire <cory@cpanel.net> - 20.6.1-1
- EA-11684: Update ea-nodejs20 from v20.6.0 to v20.6.1

* Fri Sep 08 2023 Cory McIntire <cory@cpanel.net> - 20.6.0-1
- EA-11663: Update ea-nodejs20 from v20.5.1 to v20.6.0

* Tue Aug 15 2023 Julian Brown <julian.brown@cpanel.net> - 20.5.1-1
- ZC-11127: Initial build


