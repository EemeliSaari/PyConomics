import argparse

from database import DataBase
from src.routines import check_date_routine

from server import Server

def main():
    """Main routine for software"""

    # Everytime the program is started, we check if the data is up to date
    check_date_routine()

    # Start the server
    Server(database=DataBase(), template_folder='templates').run(port=3000, debug=True)

if __name__ == '__main__':

    #TODO add more options
    parser = argparse.ArgumentParser()
    main()
