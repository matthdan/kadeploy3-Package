NAME=kadeploy
SPECFILE=$(NAME).spec

VERSION := $(shell rpm -q --qf '%{VERSION} ' --specfile $(PWD)/$(SPECFILE) | cut -d' ' -f1)
RELEASE := $(shell rpm -q --qf '%{RELEASE} ' --specfile $(PWD)/$(SPECFILE) | cut -d' ' -f1)


git:
	@echo "Clone the Git repository"
	git clone https://gforge.inria.fr/git/kadeploy3/kadeploy3.git

rake: git deps
	@echo "Run Rake build"
	cd kadeploy3
	rake
	@echo "Rake build Ok!"
tar: rake
	@echo "Get the tarball build"
	cp /tmp/kabuild/kadeploy-3.3.0.stable.tar.gz .	

rpm: deps rpmtopdirs distrules
	rpmbuild --define "_topdir $(PWD)/RPMBUILD" --define "_sourcedir $(PWD)" -ba $(SPECFILE)

distrules:
	@echo "Create Deploy Group"
	groupadd -f deploy
	@echo "Add deploy User to deploy Group"
	useradd -g deploy deploy

deps:
	yum install -y rake ruby ruby-devel rpm rpm-build mysql-devel help2man texlive
	cd $(PWD)/dependencies && $(MAKE) install

rpmtopdirs: 
	mkdir -p $(PWD)/RPMBUILD/{BUILD,RPMS,SRPMS,SPECS}

clean:
	rm -rf $(PWD)/RPMBUILD

infos:
	@echo "Informations about PACKAGE: "
	@echo "VERSION : $(VERSION)"
	@echo "RELEASE : $(RELEASE)"
