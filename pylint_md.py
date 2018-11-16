"""pylint markdown conversion tool"""

import glob
import subprocess
import json
import sys
import getopt
from collections import Counter

def pylint_markdown(location, output_path):
    """Main conversion engine"""

    totals = {'error': 0, 'warning': 0, 'refactor': 0, 'convention': 0}

    markdown_summary = list()
    markdown_summary.append('# Analysis of folder {}'.format(location))

    analysisfiles = glob.glob(location +'/**/*.py', recursive=True)
    filecount = len(analysisfiles)

    print('Analysis of {} file(s)'.format(filecount))

    markdown_files = list()
    for filepath in glob.glob(location +'/**/*.py', recursive=True):
        print('Processing file {}'.format(filepath))

        markdown_files.append('## {}'.format(filepath))
        markdown_files.append('### Summary')

        json_counter = Counter()
        lint_json = None

        proc = subprocess.Popen("pylint "+ filepath + " -f json --persistent=n --score=y",
                                stdout=subprocess.PIPE, shell=True)
        (out, _err) = proc.communicate()
        if out and  out.strip():
            lint_json = json.loads(out)
            json_counter = Counter(player['type'] for player in lint_json)

        markdown_files.append('|Type|Number|')
        markdown_files.append('|-|-|')
        markdown_files.append('|error|{}|'.format(json_counter['error']))
        markdown_files.append('|warning|{}|'.format(json_counter['warning']))
        markdown_files.append('|refactor|{}|'.format(json_counter['refactor']))
        markdown_files.append('|convention|{}|'.format(json_counter['convention']))

        # Add to the counters
        totals['error'] += json_counter['error']
        totals['warning'] += json_counter['warning']
        totals['refactor'] += json_counter['refactor']
        totals['convention'] += json_counter['convention']

        markdown_files.append('\n### Pylint messages\n')
        if lint_json is not None:
            for lint in lint_json:
                markdown_files.append('* Line: {} is {}[{}] in {}.py\n'.format(
                    lint['line'], lint['message'], lint['message-id'], lint['module']))
        else:
            markdown_files.append('* No issues found')

        markdown_files.append('---')

    # create summary

    markdown_summary.append('|Item|Number|')
    markdown_summary.append('|-|-|')
    markdown_summary.append('|files processed|{}|'.format(filecount))
    markdown_summary.append('|errors|{}|'.format(totals['error']))
    markdown_summary.append('|warnings|{}|'.format(totals['warning']))
    markdown_summary.append('|refactors|{}|'.format(totals['refactor']))
    markdown_summary.append('|conventions|{}|'.format(totals['convention']))
    markdown_summary.append('---')

    print('errors={};warnings={};refactors={};conventions={}'.format(totals['error'],
                                                                     totals['warning'],
                                                                     totals['refactor'],
                                                                     totals['convention']))

    export_as_markdown(output_path, (markdown_summary + markdown_files))

def export_as_markdown(output_path, markdown):
    """Export the markdown content"""

    print('Generating markdown file: {}'.format(output_path))
    with open(output_path, 'w') as out_file:
        for row in markdown:
            out_file.write(row+'\n')

def main(argv):
    """Main function for pylint_md to process the file arguments """

    location = None
    output_file = None
    try:
        opts, _args = getopt.getopt(argv, "hl:o:", ["rlocation=", "ooutput_file="])
    except getopt.GetoptError:
        print('pylint_md.py -l <location> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('pylint_md -l <location> -o <output_file>')
            sys.exit()
        elif opt in ("-l", "--llocation"):
            location = arg
        elif opt in ("-o", "--oooutput_file"):
            output_file = arg
    print('Location  is {}'.format(location))
    print('Output file is {}'.format(output_file))

    if location is not None and output_file is not None:
        pylint_markdown(location, output_file)

if __name__ == "__main__":
    main(sys.argv[1:])
