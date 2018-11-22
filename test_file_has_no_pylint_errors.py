"""pylint dynamic pytest wrapper"""

import glob
import subprocess
import json
import pytest

LOCATION = '.'
ANALYSIS_FILES = glob.glob(LOCATION +'/**/*.py', recursive=True)
@pytest.mark.parametrize('filepath', ANALYSIS_FILES)

def test_file_has_no_pylint_errors(filepath):
    """validate that there are zero pylint warnings against a python file"""
    print('creating tests for file {}'.format(filepath))

    proc = subprocess.Popen("pylint "+ filepath + " -f json --persistent=n --score=y",
                            stdout=subprocess.PIPE, shell=True)
    (out, _err) = proc.communicate()

    lint_json = []
    if out and  out.strip():
        lint_json = json.loads(out)

    # pylint: disable=C1801
    assert len(lint_json) == 0
