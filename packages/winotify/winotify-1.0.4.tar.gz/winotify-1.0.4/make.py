import os

from twine.__main__ import main as tw_main
from PyInstaller.__main__ import run
import sys


def exe():
    run(['winotify.py', '-F', '--distpath', 'exe'])
    print('OK')
    run(['winotify.py', '-F', '-W', '--distpath', 'exe', '-n', 'winotify-nc'])


def upload():
    sys.argv[1:] = ['upload', r'dist\*']
    sys.exit(tw_main())


def build():
    for file in os.scandir('dist'):
        os.remove(file.path)
    sys.argv[1:] = ['sdist', 'bdist_wheel']
    import setup


if __name__ == '__main__':
    if len(sys.argv) > 1:
        func = globals()[sys.argv[1]]
        if sys.argv[1] in globals() and callable(func):
            func()

