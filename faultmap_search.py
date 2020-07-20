import glob

class faultmap_file_extraction:
  def __init__(self, path, filetype):
    self.path = path
    self.filetype = filetype

    files = glob.glob(path + filetype, recursive=True)

    # use .replace to remove path from file names
    files_cleaned = [file.replace(path, '') for file in files]

    # use .partition to extract a list of all the first folder names
    #                           first partition using "\\" target
    #                                          specify which element in the partition to extract - 2nd element is the string after the target "\\"
    #                                              do a second partition with the target "\\" and this time extract the elemtn before the target
    self.files_list = [
        [file.partition("\\")[2].partition("\\")[0] for file in files_cleaned],
        [file for file in files_cleaned]
    ]
    # use set() to filter out unique entries an convert back to a list
    self.file_search_options = list(set(self.files_list[0]))

  def main_file_list(self):
    return self.files_list

  def first_level_folder_options(self):
    return self.file_search_options

if __name__ == "__main__":
    print('local test')