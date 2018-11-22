"""pylint dynamic pytest tool"""

import glob
import subprocess
import json
import sys
import getopt
from collections import Counter
import pytest
import warnings


location = '.'
analysisfiles = glob.glob(location +'/**/*.py', recursive=True)
@pytest.mark.parametrize('filepath',analysisfiles )

def test_file_has_no_pylint_errors(filepath):
    print('creating tests for file {}'.format(filepath))
    lint_json = []

    proc = subprocess.Popen("pylint "+ filepath + " -f json --persistent=n --score=y",
                            stdout=subprocess.PIPE, shell=True)
    (out, _err) = proc.communicate()
    if out and  out.strip():
        lint_json = json.loads(out)

    if lint_json is not None:
        for lint in lint_json:
            warnings.warn('Line: {} is {}[{}] in {}.py\n'.format(
                lint['line'], lint['message'], lint['message-id'], lint['module']))

    assert len(lint_json) == 0 
