from optparse import OptionParser

from database import DataBase
from src.routines import check_date_routine

from server import Server

def main():
    """
    Main routine for software
    """
    # Check the state of the database
    db = DataBase()
    # Everytime the program is started, we check if the data is up to date
    #check_date_routine()

    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port")
    (options, args) = parser.parse_args()

    #TODO add more options

    # Start the server
    Server(database=db, template_folder='templates').run(port=3000, debug=True)


if __name__ == '__main__':
    main()
