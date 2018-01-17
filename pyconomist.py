from optparse import OptionParser

from init import initialize
from src.routines import check_date_routine

def main():
    """
    Main routine for software
    """
    initialize()

    try:
        # Everytime the program is started, we check if the data is up to date
        check_date_routine('.local/')
    except OSError:
        # In case data is missing - get it.
        print("All data is missing.\n"
              "Starting the collection process...\n")
        get_data()

    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port")
    (options, args) = parser.parse_args()
    #TODO add more options

if __name__ == '__main__':
    main()
