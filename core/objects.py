from core.constants import LR_API
from munch import Munch
import requests
import imghdr
import os


# make an NFT class to hold the data
class NFT(Munch):
    def __init__(self, order_data):
        # extend the data using another api call to looksrare
        # format the parameters
        params = {
            'collection': order_data['collectionAddress'],
            'tokenId': order_data['tokenId']
        }

        # send the request
        raw = requests.get(f"{LR_API}/tokens", params=params)

        if raw.status_code != 200:
            # mark that there is no data and stop if you cannot get token data
            self.data = None
            return

        # get the json
        token_data = raw.json()['data']

        data = token_data | order_data

        # initialize the object using munch
        super().__init__(data)

    # make a function for exporting the token to a filepath
    def export(self, fp):
        # if the url is an ipfs link, reformat it to use ipfs.io
        if self.imageURI[:4] == 'ipfs':
            self.imageURI = f"https://ipfs.io/ipfs/{self.imageURI.split('://')[-1]}"

        # download the image to a folder
        img_raw = requests.get(self.imageURI)

        # don't download if unsuccessful response
        if img_raw.status_code != 200:
            return

        if len(img_raw.content) == 0:
            print('No content')

        # export the content
        export_fp = f"{fp}/{self.name}.png"
        with open(export_fp, 'wb') as outfile:
            outfile.write(img_raw.content)

        # check if the image exists --> delete it if not
        if not imghdr.what(export_fp):
            os.remove(export_fp)
