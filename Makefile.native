export EMAIL=change_me@localhost.localhost

default: release

local-loaddata:
	sed -i 's/\"is_default_site\": true/\"is_default_site\": false/g' publichealth.home.json
	python manage.py loaddata publichealth.home.json

migrate:
	. /home/app/pyvenv/bin/activate && ./manage.py migrate

migrations:
	. /home/app/pyvenv/bin/activate && ./manage.py makemigrations --merge

apply-migrations: migrations migrate

setup:
	. /home/app/pyvenv/bin/activate && ./manage.py migrate
	. /home/app/pyvenv/bin/activate && ./manage.py createsuperuser --username admin --email $(EMAIL) --noinput

rebuild:
	rm -rf node_modules
	yarn install
	cp -rf node_modules/@bower_components/* /home/app/app/publichealth/static/libs

restart-uwsgi:
	sudo /etc/init.d/uwsgi restart

compress:
	. /home/app/pyvenv/bin/activate && ./manage.py collectstatic --noinput -i media
	. /home/app/pyvenv/bin/activate && ./manage.py compress

release: rebuild compress restart-uwsgi

reindex:
	. /home/app/pyvenv/bin/activate && ./manage.py update_index

clear_index:
	elasticsearch curl -XDELETE localhost:9200/_all

django-shell:
	. /home/app/pyvenv/bin/activate && ./manage.py shell

logs:
	tail /var/log/wagtail/publichealth.log /var/log/wagtail/wagtail.log /var/log/wagtail/error.log

backup-data:
	. /home/app/pyvenv/bin/activate && ./manage.py dumpdata --natural-foreign -e auth.permission -e contenttypes -e wagtailcore.GroupCollectionPermission -e wagtailcore.GroupPagePermission -e wagtailimages.rendition -e sessions -e feedler.feedlysettings > ~/publichealth.home.json
	zip ~/publichealth.home.json.`date +"%d%m%Y-%H%M"`.zip ~/publichealth.home.json
	rm ~/publichealth.home.json

backup-images:
	echo "Backing up images ..."
	sudo chown -R app:app media
	zip -ruq ~/media.zip media

backup: backup-data backup-images

loaddata:
	. /home/app/pyvenv/bin/activate &&  ./manage.py loaddata publichealth.home.json

restore: django-loaddata restart

pg-dump:
	pg_dump -U app -d publichealth -f ./latest.sql

pg-backup:
	pg_dump -U app -d publichealth > ~/pg-backup.sql
	zip ~/pg-backup.sql.`date +"%d%m%Y-%H%M"`.zip ~/pg-backup.sql
	rm ~/pg-backup.sql

pg-restore:
	psql -U app -d publichealth -f ./latest.sql

pg-surefire-drop-restore-db:
	# drop existing database, recreate it, and then restore its content from backup.
	dropdb -h localhost -U app publichealth
	createdb -h localhost -U app publichealth
	make pg-restore
