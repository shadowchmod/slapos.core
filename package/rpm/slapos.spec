##############################################################################
#
# Copyright (c) 2010 Vifib SARL and Contributors. All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
%define slapversion 0.72
%define version 0.23
%define unmangled_version 0.23
%define unmangled_version 0.23
%define release 1


Summary:Client-side to deploy applications with SlapOS
Name: slapos.node
Version:%{slapversion}
Release:1
License:GPL
Group: Application/Network
Source0: slapos.node-%{unmangled_version}+%{slapversion}+0.tar.gz
Source1: slapprepare-%{unmangled_version}.tar.gz
URL: http://www.slapos.org/ 
Vendor: Vifib
Packager: Arnaud Fontaine <arnaud.fontaine@nexedi.com>, Cédric Le Ninivin <cedric.leninivin@tiolive.com>

BuildRequires: gcc-c++, make, patch, wget, python, chrpath, python-distribute

Requires: bridge-utils, python, gcc-c++, make, patch, wget

AutoReqProv: no


%description
 Client-side to deploy applications with SlapOS 
 SlapOS allows one to turn any application into SaaS (Service as a System),
 PaaS (Platform as a Service) or IaaS (Infrastructure as a Service) without
 loosing your freedom. SlapOS defines two types of servers: SlapOS server and
 SlapOS node.
 .
 This package contains libraries and tools to deploy a node.
 .
 Slapformat prepares a SlapOS node before running slapgrid. It then generates
 a report and sends the information to the configured SlapOS master.
 .
 Slapgrid allows you to easily deploy instances of software based on buildout
 profiles.

# Slapprepare subpackage
%package -n slapprepare
Summary: Script to prepare SlapOS
Group: Application/Network
%description -n slapprepare
Scripts to configure SlapOS easily


%prep
rm -rf $RPM_BUILD_DIR/slapprepare-%{unmangled_version}
zcat $RPM_SOURCE_DIR/slapprepare-%{unmangled_version}.tar.gz | tar -xvf -
#rm -rf $RPM_BUILD_DIR/slapos.node-%{unmangled_version}+%{slapversion}+0
#zcat $RPM_SOURCE_DIR/slapos.node-%{unmangled_version}+%{slapversion}+0.tar.gz | tar -xvf -


%build
cd $RPM_BUILD_DIR/slapprepare-%{unmangled_version}
python setup.py build
#cd $RPM_BUILD_DIR/slapos.node-%{unmangled_version}+%{slapversion}+0
#make

%install
#cd $RPM_BUILD_DIR/slapos.node-%{unmangled_version}+%{slapversion}+0
#make DESTDIR=$RPM_BUILD_ROOT install 
cd $RPM_BUILD_DIR/slapprepare-%{unmangled_version}
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
mkdir -p $RPM_BUILD_ROOT/opt/
cp -r /opt/slapos $RPM_BUILD_ROOT/opt/

%files
/
#%files -n slapprepare -f INSTALLED_FILES 
%defattr(-,root,root)

%post
echo "In order to configure SlapOS Node run slapprepare command"


