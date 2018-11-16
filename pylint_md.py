"""pylint markdown conversion tool"""

import glob
import subprocess
import json
import sys
import getopt
from collections import Counter

def pylint_markdown(root_path, output_path):
    """Main conversion engine"""

    with open(output_path, 'w') as out_file:

        out_file.write('# Analysis of folder {}\n'.format(root_path))

        analysisfiles = glob.iglob(root_path +'/**/*.py', recursive=True)

        filecount = len(list(analysisfiles))
        print('Analysis of {} file(s)'.format(filecount))
        out_file.write('\n Analysis of {} file(s)\n'.format(filecount))

        for filename in glob.iglob(root_path +'/**/*.py', recursive=True):
            print("Processing file {}".format(filename))
            out_file.write("\n## {}\n".format(filename))

            out_file.write('\n### Summary\n')

            json_counter = Counter()
            lint_json = None

            proc = subprocess.Popen("pylint "+ filename + " -f json --persistent=n --score=y",
                                    stdout=subprocess.PIPE, shell=True)
            (out, _err) = proc.communicate()
            if out and  out.strip():
                lint_json = json.loads(out)
                json_counter = Counter(player['type'] for player in lint_json)

            out_file.write('\n|Type|Number|\n')
            out_file.write('|-|-|\n')
            out_file.write('|error|{}|\n'.format(json_counter['error']))
            out_file.write('|warning|{}|\n'.format(json_counter['warning']))
            out_file.write('|refactor|{}|\n'.format(json_counter['refactor']))
            out_file.write('|convention|{}|\n'.format(json_counter['convention']))

            out_file.write('\n### Pylint messages\n\n')
            if lint_json is not None:
                for lint in lint_json:
                    out_file.write('* Line: {} is {}[{}] in {}.py\n'.format(
                        lint['line'], lint['message'], lint['message-id'], lint['module']))
            else:
                out_file.write('* No issues found\n')

            out_file.write('\n---\n')

def main(argv):
    """Main function for pylint_md to process the file arguments """

    root_path = None
    output_file = None
    try:
        opts, _args = getopt.getopt(argv, "hr:o:", ["rroot_path=", "ooutput_file="])
    except getopt.GetoptError:
        print('pylint_md.py -r <root_path> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('pylint_md -r <root_path> -o <output_file>')
            sys.exit()
        elif opt in ("-r", "--rroot_path"):
            root_path = arg
        elif opt in ("-o", "--oooutput_file"):
            output_file = arg
    print('Root Path is {}'.format(root_path))
    print('Output file is {}'.format(output_file))

    if root_path is not None and output_file is not None:
        pylint_markdown(root_path, output_file)

if __name__ == "__main__":
    main(sys.argv[1:])
