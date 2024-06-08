import requests
from bs4 import BeautifulSoup
import json

job_title = input("Please enter the job title of the job search: ")
job_location = input("Please enter the job location of the job search: ")

job_title = "%20".join(job_title.split())
job_location = "%20".join(job_location.split())


url = "https://www.linkedin.com/jobs/search?keywords=" + job_title + "&location=" + job_location + "&pageNum=0"


try:
   response = requests.get(url)
   if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    job_listings = soup.find_all('div', {'class':'job-search-card'})
    Title = []
    Company = []
    Description = []
    
    for job in job_listings:
        title = job.find('h3', {'class': 'base-search-card__title'}).text.strip()
        company = job.find('a', {'class': 'hidden-nested-link'}).text.strip()
        anchor_tag = job.find('a', class_='base-card__full-link')
        if title:
           Title.append(title)
        else:
           Title.append("N/A")
        if company:
           Company.append(company)
        else:
           Company.append("N/A")

        
        href_link = anchor_tag['href']
        print(f"Job Link: {href_link}\n")
        jobpage_response = requests.get(href_link)
        if jobpage_response.status_code == 200:
            jobpage_soup = BeautifulSoup(jobpage_response.text, 'html.parser')
            #company_line = jobpage_soup.find('a', {'class':'topcard__org-name-link topcard__flavor--black-link'})
            job_description = jobpage_soup.find('div', {'class':'description__text description__text--rich'}).text.strip()
            job_description= job_description.replace("Show more", "").replace("Show less", "").replace('\n', ' ').replace('\r', '')
            #company_link = company_line['href']
            if job_description:
               Description.append(job_description)
            else:
               Description.append("N/A")
        else:
           Description.append("N/A")
           print("Unable to open job page link.")

    print(len(Title))
    print(len(Description))
    print(len(Company))
    data = {
        "Title": Title,
        "Company": Company,
        "Job Description": Description
    }
    file_path = r"jobs.json"
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    


   else:
      print("Unable to fetch jobs.")

except requests.exceptions.HTTPError as errh:
    print ("Http Error")
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting Internet")
except requests.exceptions.Timeout as errt:
    print ("Timeout Error")
except requests.exceptions.RequestException as err:
    print ("Something Went Wrong:\n",err)
