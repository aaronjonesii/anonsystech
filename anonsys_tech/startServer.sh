FILENAME=$(date +"%m%d%Y.log")
nohup python3 manage.py runserver 93.188.164.182:22299 >> ../$FILENAME &
