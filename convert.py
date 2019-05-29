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

RELAY_STATE_LIST = [
    'RL', 'RA', 'LA', 'LL', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6'
]


ELECTRODE_FAIL_LIST = [
    'RA', 'LA', 'LL', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'x1', 'x2', 'x3', 'x4', 'x5', 'x1', 'RL'
]

LEAD_FAIL_LIST = [
    'I', 'II', 'III', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'AVR', 'AVL', 'AVF'
]


MAX_ELECTRODES_LEADS = 10

# endregion

###############################################################################
# region Function region


def convert_to_relay_header(relay_name_list):
    # Build the header for the electrode relays
    relay_header_string = ''
    for electrode_relay_string in relay_name_list:
        relay_header_string = relay_header_string + electrode_relay_string + ' Connection State, '

    # Strip junk off end...
    relay_header_string = relay_header_string[:-2]

    return relay_header_string


def convert_to_relay_state(relay_state):
    # Convert from ascii hex to number
    relay_number = int(relay_state, 16)

    # Convert relay state (really electrode state) to CSV string
    relay_state_string = ''
    for i in range(len(RELAY_STATE_LIST)):
        if relay_number & (1 << i):
            relay_state_string = relay_state_string + 'OFF, '
        else:
            relay_state_string = relay_state_string + 'ON, '

    # Strip junk off end...
    relay_state_string = relay_state_string[:-2]

    return relay_state_string


def convert_to_electrode_header(electrode_status_list):
    # Build the header for the electrode status
    electrode_status_header_string = ''
    for electrode_status_string in electrode_status_list:
        electrode_status_header_string = electrode_status_header_string + electrode_status_string + ' Electrode State, '

    # Strip junk off end...
    electrode_status_header_string = electrode_status_header_string[:-2]

    return electrode_status_header_string


def convert_to_electrode_state(electrode_state):
    # Convert from ascii hex to number
    electrode_number = int(electrode_state, 16)

    # Convert relay state (really electrode state) to CSV string
    electrode_state_string = ''
    for i in range(len(ELECTRODE_FAIL_LIST)):
        if electrode_number & (1 << i):
            electrode_state_string = electrode_state_string + 'OFF, '
        else:
            electrode_state_string = electrode_state_string + 'ON, '

    # Strip junk off end...
    electrode_state_string = electrode_state_string[:-2]

    return electrode_state_string


def convert_to_lead_header(lead_list):
    # Build the header for the electrode status
    lead_status_header_string = ''
    for lead_status_string in lead_list:
        lead_status_header_string = lead_status_header_string + lead_status_string + ' Lead State, '

    # Strip junk off end...
    lead_status_header_string = lead_status_header_string[:-2]

    return lead_status_header_string


def convert_to_lead_state(lead_state):
    # Convert from ascii hex to number
    lead_number = int(lead_state, 16)

    # Convert relay state (really electrode state) to CSV string
    lead_state_string = ''
    for i in range(len(LEAD_FAIL_LIST)):
        if lead_number & (1 << i):
            lead_state_string = lead_state_string + 'OFF, '
        else:
            lead_state_string = lead_state_string + 'ON, '

    # Strip junk off end...
    lead_state_string = lead_state_string[:-2]

    return lead_state_string


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

    relay_state_header = convert_to_relay_header(RELAY_STATE_LIST)
    electrode_state_header = convert_to_electrode_header(ELECTRODE_FAIL_LIST)
    lead_state_header = convert_to_lead_header(LEAD_FAIL_LIST)
    print(relay_state_header + ', ' + electrode_state_header + ', ' + lead_state_header)

    ###############################################################################
    # Test for existence of the LeCroy file.
    if os.path.isfile(args.csv_input_file) is False:
        print('ERROR, ' + args.csv_input_file + ' does not exist')
        print('\n\n')
        parser.print_help()
        return -1

    # Has the user specified and output file?  If not, create one for them based on the input filename.
    if args.csv_output_file is None:
        # An output file name was not given, so build one
        args.csv_output_file = os.path.splitext(os.path.basename(args.csv_input_file))[0] + '_converted.csv'

    # endregion

    # Open input CSV and read ALL the rows...
    with open(args.csv_input_file) as cvs_input_file:
        csv_reader = csv.reader(cvs_input_file)
        rows = list(csv_reader)

    # Get the reference electrode setting and wait time.
    # They will be included with the data columns 0 and 4 respectively.
    reference_electrode_setting = rows[1][0]
    wait_time = rows[1][4]

    # Okay, input file successfully opened and all the lines read, time to open the output file and start writing...
    with open(args.csv_output_file, 'w') as csv_output_file:
        # Output header information...
        print('Reference electrode: {}; wait time in seconds: {}'.format(
            reference_electrode_setting, wait_time), file=csv_output_file)
        print(relay_state_header + ', ' + electrode_state_header + ', ' + lead_state_header, file=csv_output_file)

        # Rip through all the rows (skipping first row).
        for row in rows[1:]:
            #print(row)
            relay_state = convert_to_relay_state(row[1])
            electrode_state = convert_to_electrode_state(row[2])
            lead_state = convert_to_lead_state(row[3])

            # Print the big row...
            print(relay_state + ", " + electrode_state + ', ' + lead_state, file=csv_output_file)


# endregion

###############################################################################
if __name__ == '__main__':
    rv = main()
    exit(rv)
