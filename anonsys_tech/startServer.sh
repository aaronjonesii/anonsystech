FILENAME=$(date +"%m%d%Y.log")
nohup python3 anonsys_tech/manage.py runserver 93.188.164.182:22299 >> $FILENAME &
