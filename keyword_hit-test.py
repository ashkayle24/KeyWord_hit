
# -*- coding: utf-8 -*-
import os
import subprocess
import time
import multiprocessing as mp

def hit_string(f_file):
    # 僅用來記錄讀寫的log擋
    f_log = open('D:\\temp\\f_read_log.txt', 'a+')
    f_log.write(time.strftime("%H:%M:%S") + ' Read ' + f_file)
    print(f_file)

    #取得要處裡的檔案並解壓縮
    f_file = f_file.replace('\n', '')
    f_dir = f_file[:-18]
    p = subprocess.Popen("D:\\7z.exe e " + f_file + " -oD:\\temp")
    p.wait()

    #取得要搜尋的關鍵字，並開啟關鍵字搜尋log檔
    key_word = []
    with open(r'C:\Dns_Hit\Dns_Hit.txt', "r") as f:
        for fkey in f:
            fkey = fkey.replace('\n', '')
            key_word.append(fkey)

    f_Read_temp = f_file.split('\\')
    f_Read_temp[3] = f_Read_temp[3].replace('.gz', '')
    f_each_filepath = 'D:\\temp\\' + f_Read_temp[3]
    f_hit = open('D:\\hit\\' + f_Read_temp[3], 'a+')

    #困擾的主體:讀文字檔，並拿關鍵字比對，若句子有關鍵字，就寫到上述關鍵字紀錄檔中，multiprocessing的概念嘗試
    with open(f_each_filepath, "r") as f:
        for fLine in f:
            for fkey in key_word:
                if fLine.find(fkey) != -1:
                    f_hit.write(fLine + '\n')
                    print(fLine)
    f_hit.close()

    #將上述解壓縮的檔案刪除，並寫入檔案讀寫log檔
    try:
        os.remove('D:\\temp\\' + f_Read_temp[3])
        f_log.write(time.strftime("%H:%M:%S") + ' Del ' + 'D:\\temp\\' + f_Read_temp[3] + '\r\n')
    except OSError as e:
        print(e)
    else:
        print(f_Read_temp[3] + "_File is deleted successfully")
    f_log.close()

#讀文字檔檔案路徑列表，逐行讀出並做關鍵字搜尋，用
if __name__ == '__main__':
    p = mp.Pool(processes=4)
    with open(r'D:\file_path.txt', "r") as f_file_Path:
        for f_file in f_file_Path:
            p.apply_async(hit_string,(f_file,))
    p.close()
    p.join()







