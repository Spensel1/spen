
# -*- coding: utf-8 -*-
import re
import sys

from astropy.visualization.scripts.fits2bitmap import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
