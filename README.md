# LF2CRLF
LF2CRLF: a handy python script to solve end-of-line(EOL) conversion problem

by _Yuesong Shen_

## basic examples

- convert a c file 'D:\downloaded files\unixIsTheOne.c' to have windows format EOL (CR LF)
    
    `python path\to\lf2crlf.py "D:\downloaded files\unixIsTheOne.c"`
- convert a text file '~/windowsRules.txt' to have linux/mac format EOL (LF)
    
    `python path/to/lf2crlf.py -r ~/windowsRules.txt`
- convert all files of extension _.txt_, _.py_ and _.ipynb_ in current directory and its sub-directories, disable file backup
    
    `python path\to\lf2crlf.py -i txt py ipynb -s -n`
- convert all files except extension _.pyc_ and _.exe_ in current directory, no console output unless a file bigger than 4.2 MB is to be backed up (default warning is for 1 MB, specify negative number to turn it off):
    
    `python path\to\lf2crlf.py -e pyc exe -q -w 4.2`
- the script is in current working directory. I just want to convert everything in folder `\test folder`, no backup files
    
    `python lf2crlf.py -e -s -d "test folder" -n`
    
    **attention**: a warning will be fired when you use exclusion mode without backup to warn you about the potential destructive consequences of the script.
- display full usage
    
    `python path\to\lf2crlf.py -h`
