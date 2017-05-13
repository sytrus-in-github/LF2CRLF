from __future__ import print_function
import argparse
import os


TARGET_EOL = b'\r\n' # windows
SOURCE_EOL = b'\n' # linux, mac


def convertFile(filename, backup, warnsize, verbose):
    with open(filename, 'rb') as filebody:
        filecontent = filebody.read()
    if backup:
        cancelBackup = False
        if warnsize > 0:        
            sz = getFileSize(filename)
        if sz > warnsize:
            cancelBackup = warnUser(filename, sz, warnsize)
        if not cancelBackup:
            with open(filename+'.bak', 'wb') as filebody:
                filebody.write(filecontent)
            if verbose:
                print('backup file created for '+filename)
    filecontent = filecontent.replace(SOURCE_EOL, TARGET_EOL)
    with open(filename, 'wb') as filebody:
        filebody.write(filecontent)
    if verbose:
        print('conversion done for '+filename)


def getFileSize(filename):
    with open(filename,'rb') as filebody:
        filebody.seek(0, os.SEEK_END)
        sz = filebody.tell()
    return sz

    
def warnUser(filename, sz, warnsize):
    s = ''
    while s!='y' and s!='n':
        print('type [y] or [n]')
        s = input('file '+filename+' is of size '+formatSize(sz)+', create backup file? (y/n): ')
    return s[0].lower() == 'n'

    
def formatSize(n):
    for prefix in ['','K','M','G','T','P','E','Z']:
        if n < 1024.0:
            return '{:.1f} {}B'.format(n, prefix)
        n /= 1024.0
    return '{:.1f}ZB'.format(n)


def fileIterator(includeSubdir):
    if not includeSubdir:
        for filename in os.listdir():
            if os.path.isfile(filename):
                yield filename
    else:
        for root, _, filenames in os.walk('.'):
            for filename in filenames:            
                yield os.path.join(root, filename)
            
    
if __name__=='__main__':
        
    cwd = os.getcwd()
    
    parser = argparse.ArgumentParser(description='Conversion of end-of-line (EOL) between linux/mac and windows text files.')
    parser.add_argument('filename', 
                        help='the file you want to do conversion with.', 
                        nargs='?', default=None)
    parser.add_argument('-i', '--include_ext', 
                        help='convert only files with specified extensions in current directory. If specified, <filename> argument and <-e> flag will be ignored.', 
                        nargs='+')
    parser.add_argument('-e', '--exclude_ext', 
                        help='convert files unless they have specified extensions  in current directory. If specified, <filename> argument will be ignored.', 
                        nargs='*')
    parser.add_argument('-s', '--sub_directory', 
                        help='recursively operate in all subdurectories.', 
                        action='store_true')
    parser.add_argument('-r', '--reverse', 
                        help='convert windows EOL to linux EOL.', 
                        action='store_true')
    parser.add_argument('-n', '--no_backup', 
                        help='do not create any backup file.If specified, <-w> flag will be ignored.', 
                        action='store_true')
    parser.add_argument('-w', '--warnsize', 
                        help='warn when the size of the file is bigger than the given value (in MB). Negative value to turn off.', 
                        nargs='?',type=float, default=1)
    parser.add_argument('-q', '--quiet', 
                        help='do not create any output other than warning.', 
                        action='store_true')
    parser.add_argument('-v', '--version', action='version', version='LF2CRLF by Yuesong Shen')
    args = parser.parse_args()
    # reverse targets if required
    if args.reverse:
        SOURCE_EOL, TARGET_EOL = TARGET_EOL, SOURCE_EOL
    # parse options
    includeSubDir = args.sub_directory
    nobackup = args.no_backup
    warnsize = args.warnsize
    verbose = not args.quiet
    if warnsize > 0:
        warnsize = int(round(warnsize*(2**20)))
    # operation
    if args.include_ext:
        exts = args.include_ext
        for filename in fileIterator(includeSubDir):
            if filename.split('.')[-1] in exts:
                convertFile(filename, not nobackup, warnsize, verbose)
    elif args.exclude_ext is not None:
        exts = args.exclude_ext
        if nobackup:
            s=''
            while s!='y' and s!='n':
                print('type [y] or [n]')
                s = input('Binary files with extension not specified in '+str(exts)+' may be corrupted. Proceed anyway? (y/n): ')        
            if not s[0].lower() == 'y':
                raise SystemExit('Stopped by user.')
        for filename in fileIterator(includeSubDir):
            if filename.split('.')[-1] not in exts:
                convertFile(filename, not nobackup, warnsize, verbose)
    else:
        convertFile(args.filename, not nobackup, warnsize, verbose)
