from datetime import datetime as dt
import time
import sys


def main(amount, hours_elapsed):
    # get the current date for the file path
    now = dt.utcnow()

    # get a set amount of listings between different time periods

    # make NFT objects out of each order

    # make a folder to put the nfts in

    # download each NFT (shuold do this iteratively, and ensure that you don't breach the limit --> wait one second between each request)

    pass


if __name__ == '__main__':
    amount = int(input('Amount'))
    hours_elapsed = int(input('Hours Elapsed: '))
    main(amount, hours_elapsed)
