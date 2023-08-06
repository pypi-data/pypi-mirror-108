import os
from google.colab import auth
from google.colab import drive
from zkyhaxpy.io_tools import list_files_re
import pandas as pd


def check_dup_files(folder, file_nm_prefix=None, file_nm_extension=None, remove=False):
    if file_nm_prefix==None:
        file_nm_prefix = '.*'
    if file_nm_extension==None:
        file_nm_extension = '.*'
        
    list_file_paths = list_files_re(folder, file_nm_prefix + '.*\([0-9]{1,}\)\.' + file_nm_extension)    
    
    if remove==True:
        print(f'Total of {len(list_file_paths)} duplicated files will be removed.')
        for filepath in list_file_paths:
            os.remove(filepath)
            print(f'{filepath} is removed.')
    else:   
        return list_file_paths
        
    
def mount_drive():
    drive.mount('/content/drive', force_remount=True)
    
def authen_gcp():
    auth.authenticate_user()




def list_files_re_gcs(bucket_name, client, filename_re=None, folder_re=None, path_prefix=None):
    '''
    rootpath : root path to lookup files
    filename_re : regular expression to search for filename
    folder_re : regular expression to search for folder

    return : a list of filepaths
    '''

    bucket = client.bucket(bucket_name)
    all_blobs = list(bucket.list_blobs(prefix=path_prefix))

    list_files = []
    if len(all_blobs) == 0:
        return list_files


    df_files = pd.DataFrame(all_blobs, columns=['blob'])
    df_files['path'] = df_files['blob'].astype(str).str.split(',', expand=True).loc[:, 1].str.strip()  

    if filename_re == None:
        filename_re = '.*'
    if folder_re == None:
        folder_re = '.*'
    for filepath in list(df_files['path']):   
        file_nm = os.path.basename(filepath)
        folder = os.path.dirname(filepath)
        if ((re.search(filename_re, file_nm) != None) & (re.search(folder_re, folder) != None)):
            list_files.append(os.path.join(folder, file_nm))

        
    return list_files
        
        
    