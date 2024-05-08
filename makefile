include common.mk

FORCE:

prod: tests github

github: FORCE
	- git commit -a
	git push origin master

all_tests: FORCE

dev_env: FORCE
	pip install -r $(REQ_DIR)/requirements-dev.txt

docs: FORCE
	cd $(API_DIR); make docs
