
# -*- coding: utf-8 -*-
import re
import sys

from pylint import _run_pylint_config

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(_run_pylint_config())
