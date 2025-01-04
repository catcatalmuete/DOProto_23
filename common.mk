export LINTER = flake8
export PYLINTFLAGS = --exclude=__main__.py 

PYTHONFILES = $($shell ls *.py)
PYTESTFLAGS = -vv --verbose --cov-branch --cov-report term-missing --tb=short

MAIl_METHOD = api

FORCE: 

print:
	echo "printing"

tests: lint pytests 

lint: FORCE
	cd server; $(LINTER) $(PYLINTFLAGS) *.py
	cd data; $(LINTER) $(PYLINTFLAGS) *.py

pytests: FORCE 
	cd server; export TEST_DB=1; pytest # $(PYTESTFLAGS) --cov=server
	cd data; export TEST_DB=1; pytest # $(PYTESTFLAGS) --cov=data

#test a python file:
%.py: FORCE
	$(LINTER) $(PYLINTFLAGS) $@
	export TEST_DB=1; pytest $(PYTESTFLAGS) tests/test_$*.py

nocrud:
	-rm *~
	-rm *.log 
	-rm *.out
	-rm .*swp
	-rm *.csv
	-rm $(TESTDIR)/*~
