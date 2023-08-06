# Allow conans to import ConanFile from here
# to allow refactors
import os
__version__ = '0.0.1'

HOME_DIR = os.path.join(os.path.expanduser('~'), '.epm')
HOME_DIR = os.getenv('EPM_HOME_DIR') or HOME_DIR
DATA_DIR = os.path.normpath('%s/data' % os.path.dirname(__file__))
EXTENSIONS_DIR = os.path.normpath('%s/extensions' % os.path.dirname(__file__))
DEFALT_CACHE_DIR = '.cache'
