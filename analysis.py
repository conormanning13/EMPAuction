import pandas as pd
import lxml.html
import requests

data = pd.read_csv('output.csv', skip_blank_lines=True)
data = data.dropna()
data.price = data.price.str.replace(',', '')
data.price = data.price.astype('int')


def get_artist_by_item_number(UID):
    try:
        url = 'http://auctions.emovieposter.com/'
        bidding = 'Bidding.taf?_function=detail&Auction_uid1='
        r = requests.get(url + bidding + str(UID), timeout=10)
        print(f'[{r.status_code}] Status for {UID}')
        tree = lxml.html.fromstring(r.text)
        xpath = '//*[@id="a"]/text()'
        artists = tree.xpath(xpath)[1]

        if ', ' in artists:
            artists = artists.split(', ')
        elif ' & ' in artists:
            artists = artists.split(' & ')
        elif artists == ')':
            artists = None
        else:
            pass

        return artists
    except Exception as e:
        return f'HTTP request failed: {e}'


data['artist'] = data['item_number'].apply(get_artist_by_item_number)
data['percent_of_price'] = round((data['price']/data['price'].sum() * 100), 2)

agg_dict = {
    'title': 'count',
    'price': 'sum',
    'percent_of_price': 'sum'
}
bids = data.groupby('high_bidder').agg(agg_dict)
bids = bids.sort_values(by='title', ascending=False)
sorted = data.sort_values(by='price', ascending=False)
poster_bundles = data[data.title.str.contains('group')]

full_data = pd.read_csv('with_artists.csv')
