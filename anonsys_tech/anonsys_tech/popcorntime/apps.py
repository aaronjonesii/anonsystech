from django.apps import AppConfig
import datetime

class PopcorntimeConfig(AppConfig):
    name = 'popcorntime'


def add_newentry(file, dbmoviecount):
    datestamp = datetime.datetime.now().strftime('%c')
    with open(file, 'r+') as open_file:
        file_data = open_file.read()
        open_file.seek(0, 0)
        new_entry = f"{datestamp}, {dbmoviecount}"
        open_file.write(new_entry+'\n'+file_data)
        print(f"Added new entry to file: {str(file)}")
