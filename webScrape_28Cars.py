import requests
import time
from bs4 import BeautifulSoup
import csv
import re

# Set the base URL
base_url = "https://dj1jklak2e.28car.com/sell_lst.php"

# Set the starting page and the end page
start_page = 1
end_page = 10

# Set the user-agent header
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Create a CSV file and write the headers
with open("28car.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Car Brand", "Car Model", "Year", "Status", "Price", "Engine displacement (cc)", "Uploader phone number", "Photo URL", "Description"])

    # Loop through the pages
    for page in range(start_page, end_page+1):
        url = base_url + "?page=" + str(page)
        print(url)
        response = requests.get(url, headers=headers)
        response.encoding= 'big5'
        
        # Wait for 1 second between requests
        time.sleep(1)
        
        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            pageIndex=str(page)
            # select td[height='60'] in soup
            listings = soup.select("td[height='60']")
            # Loop through the listings
            for listing in listings:
                # Get the car brand
                carBrand = listing.select("font[size='3']")
                print("carBrand:"+ carBrand[0].text)
                #return " " if no car brand
                car_brand=carBrand[0].text if carBrand and carBrand[0].text else " "

                # Get the car model
                carTd=listing.select("td[width='27%']")
                carModel=carTd[0].select("font[size='2']")
                print("carModel"+carModel[0].text)
                car_model=carModel[0].text if carModel and carModel[0].text else " "
                # carModel = listing.select("font[size='2']")

                # # Get the year and engine_cc
                yearEngineTd=listing.select("td[width='10%']")
                engine_cc=yearEngineTd[0].select("font[size='2']") if yearEngineTd and yearEngineTd[0].select("font[size='2']") else " "
                engine_cc=engine_cc[0].text.split(" ")[0] if engine_cc and engine_cc[0].text else " "
                year=yearEngineTd[1].select("font[size='2']") if yearEngineTd and yearEngineTd[1].select("font[size='2']") else " "
                year=year[0].text.split(" ")[0] if year and year[0].text else " "
                print("year:"+year)
                print("engine_cc:"+engine_cc)

                # Get the description
                desElement=listing.select("font[color='#B0B0B0']")
                description=desElement[0].text if desElement and desElement[0].text else " "
                description=description.split("，")[0]
                print("description:"+description)
                # status = listing.find("span", class_="status").text.strip()
     
                # Get the price
                priceTd=listing.select("td[width='15%']")
                price=priceTd[0].text if priceTd and priceTd[0].text else " "
                print("priceTd:"+priceTd[0].text)

                # # Get the uploader phone number
                desElement=listing.select("font[color='#B0B0B0']")
                tel=desElement[0].select("b")
                uploader=tel[0].text.split()[0] if tel and tel[0].text else " "
                print("uploader:"+uploader)
                if(len(tel)>0):
                    tel=re.findall(r'\d+',tel[0].text)
                    print("uploader tel:"+tel[0])
                else:
                    print("uploader tel: no tel")
                
                # Get the photo URL
                imgTab=listing.select("img[height='15']")
                if imgTab:
                    photo_url = imgTab[0].get('src')
                    print("photoURL:"+photo_url)
                else:
                    photo_url=""
                # Get the status
                StatuImgTab=listing.select("img[src='https://djlfajk23a.28car.com/image/sold.gif']")
                if StatuImgTab:
                    status="sold"
                else:
                    status="available"
                # Write the data to the CSV file
                writer.writerow([car_brand, car_model, year, status, price, engine_cc, uploader, photo_url, description])
        else:
            print("Request failed with status code:", response.status_code)
