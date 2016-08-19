#!/usr/bin/env bash
#Sync initial DB
echo "-=Sync intial DB: (django password)"
su - django -c "/home/django/ticketator/./manage.py makemigrations; /home/django/ticketator/./manage.py migrate"
#Create ADMIN
echo "-=Create ADMIN: (django password)"
su - django -c "/home/django/ticketator/./manage.py createsuperuser"
echo "-=Load initial DATA: (groups, states...)"
psql -d tickets_db -f  ./2_post_database_install.sql
