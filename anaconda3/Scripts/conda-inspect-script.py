
# -*- coding: utf-8 -*-
import re
import sys

from conda_build.cli.main_inspect import execute

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(execute())
