#!/bin/bash
echo "It's not who I am underneath, but what I do that defines me"
git pull origin master
echo "pulling done"
rm /home/ubuntu/apps/django_projects/meetme_prod/db.sqlite3
echo "Db removed"
/home/ubuntu/virtualenvs/meetme/bin/python /home/ubuntu/apps/django_projects/meetme_prod/manage.py migrate
echo "migration done"
/home/ubuntu/virtualenvs/meetme/bin/python /home/ubuntu/apps/django_projects/meetme_prod/manage.py test_users
echo "ok then"
