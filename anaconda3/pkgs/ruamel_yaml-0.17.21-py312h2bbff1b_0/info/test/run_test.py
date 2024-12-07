#  tests for ruamel_yaml-0.17.21-py312h2bbff1b_0 (this is a generated file);
print('===== testing package: ruamel_yaml-0.17.21-py312h2bbff1b_0 =====');
print('running run_test.py');
#  --- run_test.py (begin) ---
import os
import ruamel_yaml


try:
    import pytest
except ImportError:
    pytest = None

if pytest:
    print('ruamel_yaml.__version__: %s' % ruamel_yaml.__version__)

# version_info is used in the package
# check that it exists and matches __version__
from ruamel_yaml import version_info
ver_string = '.'.join([str(i) for i in version_info])
print(f"The ruamel_yaml version info: {ver_string}")
assert ver_string == ruamel_yaml.__version__


def pip_show():
    cmd = 'if pip show ruamel.yaml; then exit 1; fi'
    # The result will be in stdout: 'WARNING: Package(s) not found: ruamel.yaml'
    # if ruamel.yaml is not installed in the test environment
    os.system(cmd)
    print("Checked `if pip show ruamel.yaml; then exit 1; fi`")
    return

def pip_install_ruamel_dot_yaml():
    try:
        cmd = "pip install ruamel.yaml"
        os.system(cmd)
        print("Checked `pip install ruamel.yaml`")
        return
    except Exception as e:
        print(e)

def import_ruamel_dot_yaml():
    try:
        cmd = "python -c 'import ruamel.yaml'"
        os.system(cmd)
        print("Checked `python -c 'import ruamel.yaml'`")
        return
    except ImportError as e:
        print(e)
    
def pip_check():
    cmd = "pip check"
    os.system(cmd)
    print("Checked `pip check`")
    return


if __name__ == "__main__":
    if os.name != "nt":
        pip_show()
        pip_install_ruamel_dot_yaml()
        import_ruamel_dot_yaml()

    pip_check()
#  --- run_test.py (end) ---

print('===== ruamel_yaml-0.17.21-py312h2bbff1b_0 OK =====');
print("import: 'ruamel_yaml'")
import ruamel_yaml

