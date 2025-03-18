import sys

version_info = sys.version_info
major_versions = [3]
minor_versions = [8,9,10,11]
if version_info.major not in major_versions and version_info.minor not in minor_versions:
    raise (ImportError(f"ProFAST is not currenly available for your Python version ({version_info[0]}.{version_info[1]}.{version_info[2]}). ProFAST is only compatible with Python 3.8, 3.9, 3.10, 3.11"))

if version_info.minor == 8:
    from .pyc_files.ProFAST_308 import ProFAST
elif version_info.minor == 9:
    from .pyc_files.ProFAST_309 import ProFAST
elif version_info.minor == 10:
    from .pyc_files.ProFAST_310 import ProFAST
elif version_info.minor == 11:
    from .pyc_files.ProFAST_311 import ProFAST
elif version_info.minor == 12:
    from .pyc_files.ProFAST_312 import ProFAST
elif version_info.minor == 13:
    from .pyc_files.ProFAST_313 import ProFAST