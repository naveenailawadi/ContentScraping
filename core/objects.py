from munch import Munch
import requests

# make an NFT class to hold the data


class NFT(Munch):
    def __init__(self, order_data):
        # extend the data using another api call to looksrare
        raw = requests.get()

        if raw.status_code != 200:
            # mark that there is no data and stop if you cannot get token data
            self.data = None
            return

        # get the json
        token_data = raw.json()

        data = token_data | order_data

        # initialize the object using munch
        super().__init__(data)

    # make a function for exporting the token to a filepath
    def export(self, fp):
        pass
