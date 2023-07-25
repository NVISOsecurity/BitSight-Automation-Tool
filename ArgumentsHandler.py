try:
    import argparse
    import os
    import sys
    from enum import Enum
    from sys import exit
except ModuleNotFoundError as ex:
    file = str(ex).split("'")[-2]
    print(f"[-] Module '{file}' not Found! Please make sure you have installed all the dependencies correctly.")
    exit(1) 

class ArgumentHandler():
    #Replace with your groups Below.
    groups = ['{your-groups}']

    ### init function that automatically sets everything up
    ### Arguments: 
    ###         No Arguments
    ### Returns:
    ###         Nothing.
    def __init__(self):
        # Print our banner
        if not cron:
            self.print_banner()
        # Configure the parser
        parser = self.ConfigureParser()
        # Already check if no arguments are given and call help
        if len(sys.argv)==1:
            parser.print_help(sys.stderr)
            sys.exit(1)
        # Parse the arguments
        args = parser.parse_args()
        #Error Handling --- 

        if args.operation != 'update' and args.operation != 'reverse_lookup' and args.operation != 'list':
            if not args.group and not args.entity:
                print("[-] You need to specify one of the arguments --entity or --group.")
                exit(1)

        if args.operation == 'reverse_lookup' and not args.search:
            print('[-] You need to specify the IP or domain to search for. Please try again using the --search argument...')
            exit(1)

        if args.operation == 'historical':
            if not args.months:
                print('[-] You need to specifiy how many months back you want to query data for your entity. Please try again using the --months argument')
                exit(1)
        
            try:
                if int(args.months) > 12:
                    args.months = 12
                elif int(args.months) < 1:
                    print("Months cannot be less than 1. Gracefully exiting...")
                    exit(1)
            except:
                print("Months cannot be a string... Next time supply a number.")
                exit(1)

        if args.operation == 'findings' and not args.severity:
            print("Operation 'findings' requires the -s (--severity) argument. Please re-execute and specify the severity you wish to capture")
            exit(1)

        #Variable Assignments
        self.operation = args.operation
        self.group = args.group
        self.entity = args.entity
        self.severity = args.severity
        self.sort = args.sort
        self.verbose = args.verbose
        self.search = args.search
        self.months = args.months

    ### function that checks if a file exists.
    ### Arguments: 
    ###         filename: path to the file
    ### Returns:
    ###         True if the file exists, False if the file does not exist.
    def test_file(self, filename):
        try:
            with open(filename, 'r'):
                pass
            return True
        except FileNotFoundError:
            print(f"[-] {filename} not found.\nExiting...")

    ### function that prints a banner. Customize as you wish
    ### Arguments: 
    ###         No Arguments
    ### Returns:
    ###         Nothing.
    def print_banner(self):
        printBannerPadding()
        printMessage("BitSight Automation")
        printMessage("Authors: Konstantinos Papanagnou - konstantinos.papanagnou@nviso.eu")
        printBannerPadding()

    ### function that configures the parser
    ### Arguments: 
    ###         No Arguments
    ### Returns:
    ###         Nothing.
    def ConfigureParser(self):
        parser = argparse.ArgumentParser(prog='bitsight_automation.py', description='BitSight Automation script to automate certain operations like historical report generation, findings categorization, asset list retrieval, reverse lookup of IP addresses and current ratings for entites', epilog='For any questions or feedback feel free to open a GitHub Issue' )
        parser.add_argument('operation', help='The operation to perform.', choices=["rating", "historical", "findings", "assets", "reverse_lookup", 'list', "update"])
        parser.add_argument('-g', '--group', dest='group', help='The group of entities you want to query data for.', choices=self.groups)
        parser.add_argument('-e', '--entity', dest='entity', help='A specific entity you want to query data for')
        parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
        parser.add_argument('-s', '--severity', dest='severity', help='Level of Severity to be captured', choices=['All', 'Critical-High', 'Critical', 'High', 'Low', 'Medium'])
        parser.add_argument('-so', '--sort', dest='sort', help="Sort rating results either alphanumerically or alphabetically.", choices=['alphanumerically', 'alphabetically'], default='alphabetically')
        parser.add_argument('--search', dest='search', help='IP or Domain to reverse lookup for.')
        parser.add_argument('--months', dest='months', help='Add in how many months back you want to view data for. If you want 1 year, fill in 12 months. Max is 12')
        return parser

### Enumeration that holds the main 3 values for alignment purposes
class Location(Enum):
	left=1
	right=2
	center=3

try:
    cron = False
    columns = os.get_terminal_size()[0]
except OSError:
    cron = True
    print("Cron Job detected!")

# print the banner beauty
def printBannerPadding(char='='):
	print(char*columns)

# print the message inside the banner on the center
def printMessage(message, location=Location.center):
	# Calculate how many spaces we want for padding

	if location == Location.left:
		spaces = 0
	elif location == Location.right:
		spaces = columns - len(message)
	else:
		spaces = (columns - len(message)) //2

	if spaces < 0:
		spaces = 0

	print(' '*spaces + message)