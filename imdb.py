import bs4
from urllib.request import  urlopen as uReq
from bs4 import     BeautifulSoup   as soup
years = list(range(1874,2018+1))
year = years[0]

filename = "movies_imdb.csv "
f = open(filename, "w")
header = "Movie_Name ; year ; run_time ; genre ; rate ; votes    \n"
f.write(header)
for year in years :
    my_url="http://www.imdb.com/search/title?release_date=" + str(year)
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.findAll("div",{"class":"lister-item-content"})
    if len(containers) != 0 :
        container = containers[0]
        for container in containers :
            name = container.h3.a.text.replace(";",",")
            yea = container.h3.find("span",{"class":"lister-item-year text-muted unbold"}).text.replace("(","").replace(")","")
            yee = yea.strip("–")
            pp = container.p
            tt = pp.find("span",{"class":"runtime"})
            gg = pp.find("span",{"class":"genre"})
            mm = container.findAll("p")
            if  tt is   not None:
                time = tt.text
            if tt is None :
                time = "NA"
            if gg is not None :
                genre = gg.text.strip()
            if gg is None :
                genre = "NA"

            try :
                rate = container.div.div.strong.text
            except :
                rate = "NA"
            if mm is not None :
                try:
                    vv = mm[3]
                    kk= vv.find("span",{"name":"nv"}).text
                    votes = kk.replace("\nVotes:\n","").strip()
                except IndexError:
                    votes = "NA"
            if mm is None :
                votes = "NA"
            print(str(year))
            f.write( name  + ";" + yee + ";" + time + ";" + genre + ";" + rate + ";"  + votes + ";"   + "\n")

f.close()
