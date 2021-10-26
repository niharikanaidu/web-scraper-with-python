import pandas as pd
from datetime import datetime
from time import *
import requests
from bs4 import BeautifulSoup


def get_url(position, location):
    # Generate url from position and location
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    template = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={position}&txtLocation={location}"
    url = template.format(position, location)
    print(f"URL : {url}")
    return url


def main(position, location):
    # Run the main program routine
    job_titles = []
    companys = []
    job_locations = []
    salarys = []
    descriptions = []
    job_urls = []
    url = get_url(position, location)

    # Extract the job data
    sleep(1)
    print("Requesting", end="")
    seq = 2
    for i in range(0, 4):
        sleep(0.7)
        print('.', end="")
    while True:
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")

        print("\nLets start scraping")
        cards = soup.find_all("li", {"class": "clearfix job-bx wht-shd-bx"})
        for card in cards:
            try:
                title = card.find("strong", {"class": "blkclor"}).text
                job_titles.append(title)

            except:
                title = card.find("h2").text
                job_titles.append(title)

            company = card.find("h3", {"class": "joblist-comp-name"}).text.replace("\n", " ")
            companys.append(company)

            location = card.find("ul", {"class": "top-jd-dtl clearfix"})
            for loc in location:
                try:
                    a = loc.find("span").text
                    if type(a) == "int":
                        pass
                    else:
                        job_locations.append(a)
                except:
                    pass

            description = card.find("ul", {"class": "list-job-dtl clearfix"}).text.replace("\n", " ")
            descriptions.append(description)

            job_url = card.h2.a.get("href")
            job_urls.append(job_url)

            try:
                salary = card.find('i', {"class": "material-icons rupee"}).text
                if salary is not None:
                    salarys.append(salary)
                    pass
            except Exception:
                salarys.append("Not mentioned")

        try:
            url = f"https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=python&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&txtLocation=chennai&luceneResultSize=25&postWeek=60&txtKeywords=python&pDate=I&sequence={seq}&startPage=1"
            seq += 1

        except AttributeError as e:
            pass

    sleep(1)
    print("Data saving, Please wait a moment")

    # Save the job data
    df = pd.DataFrame(
        {'job_title': job_titles, 'company': companys, 'job_location': job_locations, 'job_description': descriptions,
         'job_url': job_urls, 'salary': salarys})

    df.to_csv('job2.csv', index=False, encoding='utf-8')


if __name__ == "__main__":
    position = input("Enter your position : ")
    location = input("Enter your location : ")
    main(position, location)
    sleep(2)
    print("Task completed ...!")
