"""Returns list of active files across three distributions folders"""

import pathlib
import os
import time
import datetime
from functools import wraps


def timeit(function):
    """Decorator to time a function"""
    @wraps(function)
    def wrapper(*args, **kwargs):
        print('==Start Timer==')
        start = time.time() * 1000.0
        function(*args)
        end = time.time() * 1000.0
        print(f'{function.__name__} took {int(end-start)} '
              f'milliseconds to complete')
    return wrapper

@timeit
def main():

    top_folder_path = pathlib.Path(
        r'C:\Users\jmscl\Programming\petprojects\folderwalking\Requests')

    created_date = files_in_process(top_folder_path)

    list_creation(created_date)

    prev_day_comparison(created_date)

    completed_files = completed_day_calculation(created_date)

    completed_list_update(completed_files)


def files_in_process(top_folder_path):
    """Return in process files."""

    final_total = 0
    folder_names_count = []
    created_date = []
    for folder_path in top_folder_path.glob('**\*.txt'):
        result = str(folder_path).split('\\')
        folder = result[-2]
        folder_names_count.append(folder)
        file_name = result[-1][:-4]
        if file_name not in created_date:
            path = os.path.abspath(folder_path)
            created_time = time.gmtime(os.path.getctime(path))
            created_time = time.strftime("%m/%d/%y", created_time)
            created_date.append((file_name, created_time))
        final_total += 1
    folder_names_set = set(folder_names_count)
    print('There are {} files in process'.format(final_total))
    for folder in folder_names_set:
        file_count = folder_names_count.count(folder)
        print('{} files in {}'.format(file_count, folder))
    return created_date


def list_creation(created_date):
    """saves list to file"""

    created_date.sort(key=lambda x: x[1])
    f = open('current_day.txt', 'w')
    for i in created_date:
        f.write(i[0] + ' ' + i[1] + '\n')
    f.close()


def prev_day_comparison(created_date):
    """Creates lists for the current day and the ongoing completed list"""

    g = open('completed.txt', 'r')
    line_g = g.readline()
    check_list_completed = []
    for line_g in g:
        parts = line_g.split(' ')
        check_list_completed.append(parts[0])
    g.close()
    g = open('completed.txt','a')
    for i in created_date:
        if i[0] in check_list_completed:
            pass
        else:
            g.write(i[0] + ' ' + i[1] +'\n')
    g.close()


def completed_day_calculation(created_date):
    """returns days from created date to current day for completed files"""

    g = open('completed.txt', 'r+')
    line_g = g.readline()
    name_created_date = [i[0] for i in created_date]
    today = datetime.date.today()
    completed_files = []
    for line_g in g:
        split_line_g = line_g.split(' ')
        if split_line_g[0] not in name_created_date:
            date_formatted = split_line_g[1].rsplit('\n')
            split_line_g[1] = date_formatted
            date_formatted_parts = date_formatted[0].split('/')
            file_create_date = datetime.date(2000 +
                                             int(date_formatted_parts[2]),
                                             int(date_formatted_parts[0]),
                                             int(date_formatted_parts[1])
                                             )
            time_in_progress = today - file_create_date
            completed_item = [split_line_g[0], date_formatted[0],
                  today.strftime('%m/%d/%y'),
                  str(time_in_progress)]
            completed_files.append(completed_item)
            #add removal of completed files after testing
        else:
            pass
    g.close()
    return completed_files


def completed_list_update(completed_files):
    """adds competed date to the files on the completed.txt"""
    with open('completed.txt', 'r+') as completed_txt_contents:
        completed_data = completed_txt_contents.readlines()
    completed_data = [file.split(' ') for file in completed_data]
    for file in completed_files:
        file[0] in [elem for sublist in completed_data for elem in sublist]



main()
