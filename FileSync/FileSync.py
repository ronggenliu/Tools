import os
import stat
import datetime as dt
import argparse
from pprint import pprint
import subprocess


lastmodified_file_name = 'lastmodified.txt'

def print_files(num_files, directory):
    modified = []
    rootdir = os.path.join(os.getcwd(), directory)
    lastmodified_date = readLastModifiedDate()
    for root, sub_folders, files in os.walk(rootdir):
        for file in files:
            if file.endswith(('.cpp', '.hpp', '.txt')):
                try:
                    filename = os.path.join(root, file)
                    modified_time = os.stat(os.path.join(root, file))[stat.ST_MTIME]
                    human_modified_time = dt.datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')
                    modified.append((human_modified_time, filename))
                except:
                    pass
    modified.sort(key=lambda a: a[0], reverse=True)
    modified = filter(lambda x: (dt.datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S') > dt.datetime.strptime(lastmodified_date, '%Y-%m-%d %H:%M:%S')
        and 'lastmodified.txt' not in x[1]), modified)
    print('Modified')
    pprint(modified)
    for item in modified:
        slash = item[1].rfind('./')
        subprocess.call(['cp', '--parents', item[1][slash:], 'Y:/ne3sadapt'])
    if(len(modified) > 0):
        lastmodified_date = modified[0][0]
    else:
        lastmodified_date = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    persistLastModifiedDate(lastmodified_date)

def persistLastModifiedDate(str):
    f = open(lastmodified_file_name, 'w+')
    f.write(str)
    f.close()

def readLastModifiedDate():
    f = open(lastmodified_file_name, 'r')
    lastmodified_date = f.read()
    f.close()
    return lastmodified_date

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n',
    '--number',
    help='number of items to return',
    type=int,
    default=1)
    parser.add_argument('-d',
    '--directory',
    help='specify a directory to search in',
    default='./')
    parser.add_argument('--init', dest='init', action='store_true')
    parser.add_argument('--not-init', dest='init', action='store_false')
    parser.set_defaults(init=False)
    args = parser.parse_args()
    if(args.init):
        persistLastModifiedDate(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        print_files(args.number, args.directory)

if __name__ == '__main__':
    main()