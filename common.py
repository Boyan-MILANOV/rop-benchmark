#!/usr/bin/env python3

import sys
import re
from os.path import basename

all_output_file = sys.argv[1]

with open(all_output_file, 'r') as f:
    lines = f.read().splitlines()

# set -> instrument -> result
ok_results = {}

tool_regexp = re.compile("=== Tool '(.*)' === Exp. type '(.*)' === Test suite '(.*)'.*")
bin_regexp = re.compile(".*:rop-benchmark:(.*):(.*) - (.*) - (.*)")
tool, test_suite = None, None
for line in lines:
    m = tool_regexp.match(line)
    if m:
        tool, test_suite = m.group(1), m.group(3)
        if test_suite not in ok_results:
            ok_results[test_suite] = {}
        if tool not in ok_results[test_suite]:
            ok_results[test_suite][tool] = set()
        continue

    m = bin_regexp.match(line)
    if m:
        tool_r, binary, log_level, status = m.group(1), m.group(2), m.group(3), m.group(4)
        assert tool_r == tool, "MISMATCH tool {} != {}".format(tool_r, tool)
        if log_level == "INFO" and status == "OK":
            ok_results[test_suite][tool].add(basename(binary))

common = {}
for test_suite, ts_dic in ok_results.items():
    common[test_suite] = set()
    for tool, results in ts_dic.items():
        for binary in results:
            common[test_suite].add(binary)
    print("Common for {} consists of {} binaries".format(test_suite, len(common[test_suite])))
    # print(common[test_suite])

if len(sys.argv) > 2:
    diff_tool = sys.argv[2]
    print("Possible improvements for {}".format(diff_tool))
    for test_suite, ok_all in common.items():
        diff = ok_all - ok_results[test_suite][diff_tool]
        print("Test suite {}".format(test_suite))
        print(diff)

