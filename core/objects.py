from core.constants import LR_API
from munch import Munch
import requests


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
        if self.tokenURI[:4] == 'ipfs':
            self.tokenURI = f"https://ipfs.io/ipfs/{self.tokenURI.split('://')[-1]}"

        # get the metadata
        raw = requests.get(self.tokenURI)

        # skip if you can't get any metadata
        if raw.status_code != 200:
            return

        # get the image url
        img_url = raw.json()['image']

        # make an image name
        img_name = f"{self.name}.png"

        # download the image to a folder
        img_raw = requests.get(image_url)

        # don't download if unsuccessful response
        if img_raw != 200:
            return

        # export the content
        with open(f"{fp}/{img_name}", 'wb') as outfile:
            outfile.write(img_raw.content)
