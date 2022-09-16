from core.constants import LR_API
from core.objects import NFT
from datetime import datetime as dt
import requests
import json
import time


def main(amount, hours_elapsed):
    # get the current date for the file path
    now = dt.now()

    # get the seconds elapsed from the hours elapsed
    secs_elapsed = hours_elapsed * 60 * 60

    # get a set amount of listings between different time periods
    params = {
        'startTime': int(time.time() - secs_elapsed),
        'endTime': int(time.time()),
        'pagination': json.dumps({
            'first': amount
        }),
        'sort': 'PRICE_DESC'  # want to sort descending to get the coolest NFTs
    }
    raw = requests.get(f"{LR_API}/orders", params=params)

    # return if you can't get any NFTs
    if raw.status_code != 200:
        print('Failed to get NFT orders.')
        return

    # get the orders
    orders = raw.json()['data']

    # make a folder to put the nfts in
    folder = f"{now.year}-{now.month}-{now.day} ({hours_elapsed})"

    # make NFT objects out of each order
    for order in orders:
        start = time.time()

        # make the nft
        nft = NFT(order)

        # export the nft to a folder
        nft.export(folder)

        # make sure at least a second elapses between requests
        time.sleep(max(1 - (time.time() - start), 0))


if __name__ == '__main__':
    amount = int(input('Amount: '))
    hours_elapsed = int(input('Hours Elapsed: '))
    main(amount, hours_elapsed)
