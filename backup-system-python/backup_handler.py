'''
Description:
  This application will backup files from given directory and save to destination folder.
  Files/Directories in .gitignore will be ignored.
  Files/Directories in backup_ignore.txt will be ignored.

  TODO List:
    - implement feature: if a file is used, keep record of it and come back to it later on
    - implement feature: pick up where it left off during previous backup session, if ended before finishing
    - generate logs of successful backup and failed backups
    - generate test cases
    - 
'''

import os
import platform
import shutil

class BackupHandler():
  def __init__(self, source_path, destination_path) -> None:
    self.source_path = source_path
    self.destination_path = destination_path
    self.gitignore_keys = None
    self.ignored_list_file = 'ignored_files.txt'
    self.ignore_dict = self.get_ignore_dict()
    self.add_gitignore_to_ignore_dict()
  
  def get_ignore_dict(self):
    ignore_dict = {}
    if os.path.isfile(self.ignored_list_file):
      with open(self.ignored_list_file, 'r') as f:
        file_paths = f.readlines()
        for file_path in file_paths:
          filtered_path = file_path.strip()
          ignore_dict[filtered_path] = ''
    return ignore_dict

  def add_to_ignore_list(self, ignored_file):
    ignored_path = self.source_path + ignored_file
    if ignored_path not in self.ignore_dict:
      with open(self.ignored_list_file, 'a+') as f:
        f.write(ignored_path + '\n')
      self.ignore_dict[ignored_path] = ''

  def add_gitignore_to_ignore_dict(self):
    with open('.gitignore') as f:
      ignore_lines = f.readlines()
      for ignore_line in ignore_lines:
        filtered_path = ignore_line.strip()
        if len(filtered_path) >= 1:
          platform_path = '/'
          if platform.system() == 'Windows':
            platform_path = '\\'
          gitignore_line = '{0}{1}{2}'.format(self.source_path, platform_path, filtered_path)
          self.ignore_dict[gitignore_line] = ''

  def get_source_file_list_from_source_root(self, source_root, source_list):
    # if it's a directory, then list out paths and go one level down
    if not os.path.isfile(source_root):
      sub_paths = os.listdir(source_root)
      for sub_path in sub_paths:
        sub_full_path = '{0}/{1}'.format(source_root, sub_path)
        source_list = self.get_source_file_list_from_source_root(source_root=sub_full_path, source_list=source_list)
    else:
      # else it is a file, so add to source_list
      if source_root not in self.ignore_dict:
        source_list.append(source_root)
    return source_list
  
  def get_destination_list_from_source_list(self, source_list, source_root, destination_root):
    destination_list = []
    for source_path in source_list:
      sub_path = source_path.split(source_root)[1]
      destination_path = '{0}/{1}'.format(destination_root, sub_path)
      destination_list.append(destination_path)
    return destination_list
  
  def copy_files(self, source, destination):
    # populate files list with fullpaths from source
    source_list = self.get_source_file_list_from_source_root(source_root=source_path, source_list=[])
    destination_list = self.get_destination_list_from_source_list(source_list=source_list, source_root=source, destination_root=destination)
    print(destination_list)

    if len(source_list) == len(destination_list):
      i = 0
      while i < len(source_list):
        # match sub directories from source to destination
        os.makedirs(os.path.dirname(destination_list[i]), exist_ok=True)
        shutil.copy(source_list[i], destination_list[i])
        i += 1

if __name__ == '__main__':
  source_path = os.getcwd() + '/source_files'
  destination_path = os.getcwd() + '/destination_files'
  tester = BackupHandler(source_path=source_path, destination_path=destination_path)
  source_list = tester.copy_files(source=source_path, destination=destination_path)
