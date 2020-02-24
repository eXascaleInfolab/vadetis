#!/usr/bin/python

import sys, getopt, csv
from datetime import datetime, timedelta


def main(argv):
    inputfile = None
    outputfile = None
    try:
        opts, args = getopt.getopt(argv, "hf:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -f <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -f <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-f", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    print('Input file is ', inputfile)
    print('Output file is ', outputfile)

    transform(inputfile, outputfile)

def transform(inputfile, outputfile):
    print('transforming')
    start_time = datetime.now().replace(year=2018, microsecond=0, second=0, minute=0)
    header = ['ts_name', 'time', 'unit', 'value', 'class']
    with open(inputfile, 'r') as file_input, open(outputfile, 'w') as file_output:
        writer = csv.writer(file_output, delimiter=';')
        writer.writerow(header)
        count = 0
        while True:
            count += 1
            # Get next line from file
            line = file_input.readline()

            # if line is empty end of file is reached
            if not line:
                print('transforming done')
                break
            else:
                ts_values = line.split()
                ts_name = 'Series' + '{:02d}'.format(count)
                time = start_time
                for value in ts_values:
                    row = [ts_name, format(time, '%Y%m%d%H%M'), 'Value', value, 0]
                    writer.writerow(row)
                    time = time + timedelta(hours=1)

            #print("Line{}: {}".format(count, line.strip()))


if __name__ == "__main__":
    main(sys.argv[1:])
