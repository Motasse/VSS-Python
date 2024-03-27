from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import sys, json, urllib.request, urllib.error, urllib.parse, gzip, csv

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] != "--execute":
        print("FATAL Unsupported execution mode (expected --execute flag)", file=sys.stderr)
        sys.exit(1)
    else:
        #settings = json.loads(sys.stdin.read())
        result = sys.stdin.read()
        payload = json.loads(result)

        f=gzip.open(payload['results_file'], 'rt', newline='')
        file_content=f.read()

        file = open("testResult.txt", "w")
        file.write(str(file_content))
        file.close()

        print("here we go", payload)
        sys.exit(0)