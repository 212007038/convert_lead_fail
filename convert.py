#
# Python script to convert LabView CSV ECG lead fail test output to a more "filterable" version.
#
#
# region Import region
import os
import argparse  # command line parser
import csv
# endregion

###############################################################################
# region Variables region
###############################################################################
__version__ = '1.0'  # version of script

RELAY_STATE = [
    'RL', 'RA', 'LA', 'LL', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6'
]


ELECTRODE_FAIL = [
    'RA', 'LA', 'LL', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'x1', 'x1', 'x1', 'x1', 'x1', 'x1', 'RL'
]

LEAD_FAIL = [
    'I', 'II', 'III', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'AVR', 'AVL', 'AVF'
]


MAX_ELECTRODES_LEADS = 10

# endregion

###############################################################################
# region Function region
def convert_to_relay_state(relay_state):
    # Convert from ascii hex to number
    relay_number = int(relay_state, 16)

    # Convert relay state (really electrode state) to CSV string
    for i in range(MAX_ELECTRODES_LEADS):
        if relay_number


def convert_to_electrode_state(electrode_state):

def convert_to_lead_state(lead_state):



###############################################################################
# endregion

###############################################################################
# region Main region
def main(arg_list=None):
    """The main function of this module.

    Perform all the processing on a LeCroy CSV exported active cable capture.
    Returns the timing metrics on the capture data.

    """
    ###############################################################################
    # region Command line region

    ###############################################################################
    # Setup command line argument parsing...
    parser = argparse.ArgumentParser(description="Process an exported LeCroy CSV file (from spreadsheet view)")
    parser.add_argument('-i', dest='csv_input_file',
                        help='name of LabView ECG lead fail CSV result file', required=True)
    parser.add_argument('-o', dest='csv_output_file',
                        help='name of CSV output file to write new ecg lead fail statistics to', required=False)
    parser.add_argument('-v', dest='verbose', default=False, action='store_true',
                        help='verbose output flag', required=False)
    parser.add_argument('--version', action='version', help='Print version.',
                        version='%(prog)s Version {version}'.format(version=__version__))

    # Parse the command line arguments
    args = parser.parse_args(arg_list)

    ###############################################################################
    # Test for existence of the LeCroy file.
    if os.path.isfile(args.csv_input_file) is False:
        print('ERROR, ' + args.csv_input_file + ' does not exist')
        print('\n\n')
        parser.print_help()
        return -1

    # endregion

    # Open input CSV...
    with open(args.csv_input_file) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')

        # Read the header.
        headers = next(read_csv, None)
        print('HEADERS: {}'.format(headers))

        # Now process the rest...
        for row in read_csv:
            relay_state = convert_to_relay_state(row[1])
            electrode_state = convert_to_electrode_state(row[2])
            lead_state = convert_to_lead_state(row[3])



# endregion

###############################################################################
if __name__ == '__main__':
    rv = main()
    exit(rv)
