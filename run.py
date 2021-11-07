# Import libraries
from urllib.request import  urlopen 
from bs4 import BeautifulSoup as soup
from datetime import date 
import argparse
from tqdm import trange
from re import sub

parser=argparse.ArgumentParser()

parser.add_argument('-s', '--start', help='Start year (1874 by default)')
parser.add_argument('-e', '--end', help='End year (current year by default')
parser.add_argument('-o', '--output', help='Output file name (Movies from <start> to <end>.csv by default')

args = parser.parse_args()

# Define default values
DEFAULT_START = 1874
DEFAULT_END = date.today().year

start_date = DEFAULT_START if not args.start else int(args.start)
end_date = DEFAULT_END if not args.end else int(args.end)

DEFAULT_FILE_NAME = f'Movies from {start_date} to {end_date}.csv'
file_name = DEFAULT_FILE_NAME if not args.output else args.output
if not file_name.endswith('.csv'):
    file_name += '.csv'

# Define functions
def handle_none(obj):
    return "NA" if obj is None else obj.text.strip()

def write_movies(file, year_):
    url = f'http://www.imdb.com/search/title?release_date={year_}'
    client = urlopen(url)
    html_page = client.read()
    client.close()
    soup_page = soup(html_page, "html.parser")
    movies = soup_page.findAll("div",{"class":"lister-item-content"})
    for movie in movies:
        name = movie.a.text.replace(';',',')
        year = movie.find("span",{"class":"lister-item-year text-muted unbold"}).text
        year = sub('[^0-9–]', '', year)
        time_span = movie.find("span",{"class":"runtime"})
        genre_span = movie.find("span",{"class":"genre"})
        votes_span = movie.find("span",{"name":"nv"})
        time = handle_none(time_span)
        genre = handle_none(genre_span)
        rate = handle_none(movie.strong)
        votes = handle_none(votes_span)
        file.write(';'.join([name, year, time, genre, rate, votes]) + '\n')

# Initialize file head

if __name__ == '__main__':

    file = open(file_name, 'w', encoding = 'utf-8')
    columns = ['Movie Name', 'Release Year', 'Run Time' , 'Genre', 'Rate', 'Votes']
    file.write(';'.join(columns) + '\n')

    for year_ in trange(start_date, end_date + 1):
        write_movies(file, year_)
    file.close()