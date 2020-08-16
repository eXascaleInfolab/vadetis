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
    header = ['ts_name', 'time', 'unit', 'value', 'class']
    read_header = ['stn', 'time', 'tso005s0']
    with open(inputfile, 'r') as file_input, open(outputfile, 'w') as file_output:
        reader = csv.reader(file_input, delimiter=';')
        next(reader, None)  # skip the headers
        writer = csv.writer(file_output, delimiter=';')
        writer.writerow(header)

        for row in reader:
            row = [row[0], row[1], 'Celsius', row[2], 0]
            writer.writerow(row)

        print('transforming done')


if __name__ == "__main__":
    main(sys.argv[1:])
