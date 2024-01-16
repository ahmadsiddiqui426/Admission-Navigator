from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin

url = 'https://www.eduvision.edu.pk/programs-offered-in-computer-sciences-information-technology-at-bachelor-level-in-pakistan'
r = requests.get(url, verify=False)

htmlContent = r.text
soup = BeautifulSoup(htmlContent, "html.parser")
divs = soup.find("div", class_="col-xs-12", style=" padding:0; background: #b5e9ff;")
lis = divs.find_all("li",class_="list-group-item d-flex align-items-center col-lg-12 col-md-12 col-sm-12 col-xs-12 li-dis", style="padding:5px 2px; verticle-align:middle;")
fields = list()
with open(r"C:\\Users\\lenovo\\OneDrive\\Desktop\\ConsoleApp1\\ConsoleApp1\\bin\\Debug\\net6.0\\Files\\fields.csv", "w") as file:

    #file.write("Name\n")
    for i, li in enumerate(lis):
        anchor_tags = li.find("a")
        if anchor_tags.text:
            file.write(f"{anchor_tags.text}\n")
            fields.append(anchor_tags.text)

for i, field in enumerate(fields):
    f = field.lower().replace(" ", "-")
    fieldurl = f"https://www.eduvision.edu.pk/institutions-offering-{f}-with-field-computer-sciences-information-technology-at-bachelor-level-in-lahore-page-1"
    res = requests.get(fieldurl, verify=False)
    fieldContent = res.text
    soup2 = BeautifulSoup(fieldContent, "html.parser")
    table = soup2.find("table")

    table_entries = []  # A list to store the table data
    if table:
        rows = table.find('tbody', class_='para').find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            institute = cols[0].get_text(strip=True)
            city = cols[1].get_text(strip=True)
            degree_duration = cols[2].get_text(strip=True)
            fee = cols[3].get_text(strip=True)
            deadline = cols[4].get_text(strip=True)
            
            # Append the data to the list
            table_entries.append(f"{institute}, {city}, {fee}, {deadline}")

        # Print the scraped data
            with open(f"C:\\Users\\lenovo\\OneDrive\\Desktop\\ConsoleApp1\\ConsoleApp1\\bin\\Debug\\net6.0\\Files\\Universities\\uni{i+1}.csv", "w") as file:
                #file.write("Name, Location, Degree, Fee, Deadline\n")
                for entry in table_entries:
                    file.write(f"{entry}\n")

for i, field in enumerate(fields):
    f = field.lower().replace(" ", "-")
    admUrl = f"https://www.eduvision.edu.pk/admissions.php?discipline_type=Computer-Sciences-Information-Technology&sub_level=7&discipline={f}&city=Lahore&pageNo=1"
#fieldurl = "https://www.eduvision.edu.pk/institutions-offering-artificial-intelligence-with-field-computer-sciences-information-technology-at-bachelor-level-in-lahore-page-1"
    res = requests.get(admUrl, verify=False)
    admContent = res.text
    soup3 = BeautifulSoup(admContent, "html.parser")
    table = soup3.find("table")
    table_entries = []

    if table:
        # Specify the folder to save the images
        save_folder = f"C:\\Users\\lenovo\\OneDrive\\Desktop\\WebApplication4\\WebApplication4\\wwwroot\\images\\img{i+1}"
        os.makedirs(save_folder, exist_ok=True)

        # Find all rows in the table
        rows = table.find('tbody', class_='para').find_all('tr')
        j = 1
        # Iterate through each row
        for row in rows:
            # Find all columns in the row
            cols = row.find_all('td')

            # Find the image tag in the first column
            img_tag = cols[0].find("img", class_="img-responsive hidden-xs hidden-sm")
            auni = cols[1].find("a")
            if auni:
                uni = auni.text.replace(",", " ")
            discipline = cols[2].text.replace("\n", "")
            adate = cols[3].find("a")
            if adate:
                date = adate.text
            table_entries.append(f"{uni}, {discipline}, {date}" )
            
            # Check if the image tag is found
            if img_tag:
                # Get the source URL of the image
                img_url = img_tag.get('src')

                # Make sure the URL is absolute
                img_url = urljoin(url, img_url)

                # Send a GET request to the image URL
                img_response = requests.get(img_url)

                # Extract the image filename from the URL
                img_filename = os.path.join(save_folder, f"icon{j}.jpg")

                # Save the image to the local directory
                with open(img_filename, 'wb') as img_file:
                    img_file.write(img_response.content)
                j += 1
            with open(f"C:\\Users\\lenovo\\OneDrive\\Desktop\\ConsoleApp1\\ConsoleApp1\\bin\\Debug\\net6.0\\Files\\Admissions\\admissions{i+1}.csv", "w") as file:
                for entry in table_entries:
                    file.write(f"{entry}\n")