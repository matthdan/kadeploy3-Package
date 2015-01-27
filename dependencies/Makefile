NAME=ruby-mysql
STABLE_TARBALL=mysql-ruby-2.8.2.tar.gz
SPECFILE=$(NAME).spec

VERSION := $(shell rpm -q --qf '%{VERSION} ' --specfile $(PWD)/$(SPECFILE) | cut -d' ' -f1)
RELEASE := $(shell rpm -q --qf '%{RELEASE} ' --specfile $(PWD)/$(SPECFILE) | cut -d' ' -f1)

rpmtopdirs: 
	mkdir -p $(PWD)/RPMBUILD/{BUILD,RPMS,SRPMS,SPECS}

rpm: rpmtopdirs deps
	rpmbuild --define "_topdir $(PWD)/RPMBUILD" --define "_sourcedir $(PWD)" -ba $(SPECFILE)
	mkdir -p $(PWD)/rpms
	cp -r $(PWD)/RPMBUILD/RPMS/x86_64/$(NAME)-$(VERSION)-$(RELEASE).x86_64.rpm $(PWD)/rpms 

deps:
	yum install -y rpm rpm-build ruby-devel mysql-devel

install: rpm
	yum install -y $(PWD)/rpms/$(NAME)-$(VERSION)-$(RELEASE).x86_64.rpm

infos:
	@echo "Informations about PACKAGE: "
	@echo "VERSION : $(VERSION)"
	@echo "RELEASE : $(RELEASE)"

clean:
	rm -rf $(PWD)/RPMBUILD
	rm -rf $(PWD)/rpms