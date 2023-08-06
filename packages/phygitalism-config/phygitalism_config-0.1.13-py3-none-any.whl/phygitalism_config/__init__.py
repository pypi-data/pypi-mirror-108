import sys
from .import_loader import ImportLoader
from .import_finder import ImportFinder

loader = ImportLoader()
finder = ImportFinder(loader)
sys.meta_path.append(finder)
