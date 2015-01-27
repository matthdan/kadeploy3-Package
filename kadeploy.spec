Name:           kadeploy
Version:        3.3.0
Release:        1%{dist}
Group:          System/Cluster
License:        CeCILL V2
URL:            http://gforge.inria.fr/scm/?group_id=2026
Summary:        Package of the Kadeploy deployment tool.

%define src_dir %{name}-%{version}.stable
%define src_tarall %{src_dir}.tar.gz
Source0:		%{src_tarall}


%description
Kadeploy 3 is the next generation of the fast and scalable deployment system
for cluster and grid computing. Kadeploy is the reconfiguration system used
in Grid5000, allowing the users to deploy their own OS on their reserved nodes.

%package common
Summary:        Common part of the Kadeploy deployment tool.
Requires:       ruby, ruby-mysql, ruby-libs, mysql-devel
Group:          System/Cluster
%description common
This package provide the common part of the Kadeploy deployment tool.

%package server
Summary:        Server part of the Kadeploy deployment tool.
Requires:       ruby, ruby-mysql, kadeploy-common = %{version}
Group:          System/Cluster
%description server
This package provide the server part of the Kadeploy deployment tool.

%package client
Summary:        Client part of the Kadeploy deployment tool.
Requires:       ruby, ruby-mysql, kadeploy-common = %{version}
Group:          System/Cluster
%description client
This package provide the client part of the Kadeploy deployment tool.

%prep
%setup -q -n %{name}-%{version}.stable

%build

%install
rm -rf $RPM_BUILD_ROOT
rake install[${RPM_BUILD_ROOT},redhat]
rake install_kastafior[${RPM_BUILD_ROOT}]

%check

%clean
rm -rf $RPM_BUILD_ROOT

%files common
%defattr(-,deploy,deploy,-)
%doc License.txt README AUTHORS NEWS doc/*.pdf
#/KADEPLOY3_LIBS/*
/usr/share/ruby/vendor_ruby/kadeploy3/common/*.rb
/usr/share/ruby/vendor_ruby/kadeploy3/common.rb
%dir /etc/kadeploy3
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_defaultdocdir}/kadeploy3/scripts/*
%{_defaultdocdir}/kadeploy3/kastafior.gz
%{_defaultdocdir}/kadeploy3/kascade.gz

%files server
%dir /var/log/kadeploy3
%attr(0770,root,deploy) /var/log/kadeploy3
%dir /var/run/kadeploy3d
%attr(0740,deploy,deploy) /var/run/kadeploy3d
%defattr(-,deploy,deploy,-)
/etc/init.d/kadeploy
%config(noreplace) /etc/kadeploy3/clusters.conf
%config(noreplace) /etc/kadeploy3/sample-cluster.conf
%config(noreplace) /etc/kadeploy3/command.conf
%config(noreplace) /etc/kadeploy3/server.conf
/etc/kadeploy3/version
/usr/bin/kastafior
/usr/sbin/kadeploy3d
/usr/share/ruby/vendor_ruby/kadeploy3/server/*.rb
/usr/share/ruby/vendor_ruby/kadeploy3/server.rb

%files client
%defattr(-,deploy,deploy,-)
%config(noreplace) /etc/kadeploy3/client.conf
/usr/bin/kaconsole3
/usr/bin/kanodes3
/usr/bin/kastat3
/usr/bin/kadeploy3
/usr/bin/kaenv3
/usr/bin/kareboot3
/usr/bin/kapower3
/usr/sbin/karights3
/usr/share/ruby/vendor_ruby/kadeploy3/client/*.rb
/usr/share/ruby/vendor_ruby/kadeploy3/client.rb

%pre server
if ! getent passwd deploy >/dev/null 2>&1 ; then
  /usr/sbin/useradd --system --create-home --base-dir /var/lib deploy >/dev/null 2>&1 || exit 1
fi

%post server
chkconfig --add kadeploy

%preun server
chkconfig --del kadeploy
