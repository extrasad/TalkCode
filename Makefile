freeze:
	pip freeze | grep -v "pkg-resources" > requirements.txt

mysqlsetup:
	sudo apt-get install build-essential python-dev libmysqlclient-dev python-mysqldb

react:
	cd application && npm run start && cd..