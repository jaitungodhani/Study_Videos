#!/usr/bin/bash

sed -i 's/\[]/\["16.170.228.30"]/' /home/ubuntu/Study_Videos/study_videos/settings.py

python manage.py migrate
python manage.py makemigrations
python manage.py collectstatic
python manage.py create_groups
python manage.py import_languages
sudo service gunicorn restart
sudo service nginx restart
#sudo tail -f /var/log/nginx/error.log
#sudo systemctl reload nginx
#sudo tail -f /var/log/nginx/error.log
#sudo nginx -t
#sudo systemctl restart gunicorn
#sudo systemctl status gunicorn
#sudo systemctl status nginx
# Check the status
#systemctl status gunicorn
# Restart:
#systemctl restart gunicorn
#sudo systemctl status nginx
