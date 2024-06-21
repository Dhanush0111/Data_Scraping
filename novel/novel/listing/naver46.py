from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from csv import DictWriter
from bs4 import BeautifulSoup
import os
import time
from DrissionPage import ChromiumPage
import html
df_header = {
            "Title":[],
            "Author":[],
            "Tags":[],
            "URL":[],
            "Introduction":[],
            "Total chapters":[],
            "Downloads":[],
            "Ratings":[],
            "Likes Count":[],
            "Interests Count":[],
            "Comment Count":[],
        }

def append_list_as_row(list_of_elem):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a+", encoding="utf-8-sig", newline="") as csvfile:
        writer = DictWriter(csvfile, fieldnames=df_header)
        if not file_exists:
            writer.writeheader()
        writer.writerow(list_of_elem)

options=uc.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--cookie=aws-ubid-main=740-7370645-5242451; session-id=131-6894656-6125142; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:IN"; ubid-main=133-5129884-6918967; skin=noskin; aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Asts%3A%3A856517911253%3Aassumed-role%2FAWSReservedSSO_BackInnies_fa60f0f6242afd57%2Fparth.khandenath%40pocketfm.com%22%2C%22alias%22%3A%22radio-ly%22%2C%22username%22%3A%22assumed-role%252FAWSReservedSSO_BackInnies_fa60f0f6242afd57%252Fparth.khandenath%2540pocketfm.com%22%2C%22keybase%22%3A%22vQ99v68c4K02OcaQJMYUnJGG6MnfhVcS7vmqgTLpszE%5Cu003d%22%2C%22issuer%22%3A%22https%3A%2F%2Fpocketfm-apsoutheast-1.awsapps.com%2Fstart%2F%23%2Fsaml%2Fcustom%2F856517911253%2520%2528Radio.ly%2529%2FODU2NTE3OTExMjUzX2lucy05N2JhZTU2YWQ0Mjc4OGNmX3AtMTY2NzEwZmYyZTdiYTJlNg%5Cu003d%5Cu003d%22%2C%22signinType%22%3A%22PUBLIC%22%7D; aws-userInfo-signed=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJhcC1zb3V0aGVhc3QtMSIsImFsZyI6IkVTMzg0Iiwia2lkIjoiNzc2YjdlYTUtODRhYi00N2I0LTg1MmMtMjBhNDJjNjEwYjBlIn0.eyJzdWIiOiJyYWRpby1seSIsInNpZ25pblR5cGUiOiJQVUJMSUMiLCJpc3MiOiJodHRwczpcL1wvcG9ja2V0Zm0tYXBzb3V0aGVhc3QtMS5hd3NhcHBzLmNvbVwvc3RhcnRcLyNcL3NhbWxcL2N1c3RvbVwvODU2NTE3OTExMjUzJTIwJTI4UmFkaW8ubHklMjlcL09EVTJOVEUzT1RFeE1qVXpYMmx1Y3kwNU4ySmhaVFUyWVdRME1qYzRPR05tWDNBdE1UWTJOekV3Wm1ZeVpUZGlZVEpsTmc9PSIsImtleWJhc2UiOiJ2UTk5djY4YzRLMDJPY2FRSk1ZVW5KR0c2TW5maFZjUzd2bXFnVExwc3pFPSIsImFybiI6ImFybjphd3M6c3RzOjo4NTY1MTc5MTEyNTM6YXNzdW1lZC1yb2xlXC9BV1NSZXNlcnZlZFNTT19CYWNrSW5uaWVzX2ZhNjBmMGY2MjQyYWZkNTdcL3BhcnRoLmtoYW5kZW5hdGhAcG9ja2V0Zm0uY29tIiwidXNlcm5hbWUiOiJhc3N1bWVkLXJvbGUlMkZBV1NSZXNlcnZlZFNTT19CYWNrSW5uaWVzX2ZhNjBmMGY2MjQyYWZkNTclMkZwYXJ0aC5raGFuZGVuYXRoJTQwcG9ja2V0Zm0uY29tIn0.IafD94OK7MsDzBgB0hmZhM0lQx5O1qz2PYkf-5lCLhysfZ4uW5Y3GBp6w50FNX9C5POzNNed4lIduH0S64YlUfIGsVIY1ytpqckFj41Ba-3n2YLA7ZhX9wZkzQ1-Ecek; noflush_awsccs_sid=bb5b846d0805b435693bebe569b4f935c25378d840435f35351e727e04b7e582; lc-main=en_US; session-token=/5zE8qmQvWRorYm93rvkhHJ3dE1HFNK4LJQx2/rbrMLAbGMMfkguUmGktPgShkLjy/O5ICvn+c1+nBRs5MK/OO5E3ELThvQQhxJFDsKlQ8tVrIPpnCocJUEPOk/GQnZOzPviWCJMdxGqu/lDUOKMsIP8Pm4XHtAlP1foSOZs1H4J1n79gqBM+gfL1MG/H+a7Rq9xm4WKUrt4HB0UzjoTKpNJ3Sqo7/J0uQHHwAs4aDM0epT/Yn26n40IKvvnnd1+lGPl9DODhlKDNaadrEZLIyZzDbbVcUWbPhHsjOVwp0Ks1jMb4Gc7Me/EijPa4g+n06RjQhveoDmSDj+NLYER1J2eS8e7bGud; csm-hit=tb:s-GFV49DPRXHZCWD2PEXAD|1709126625818&t:1709126626268&adb:adblk_no')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36')
# driver = uc.Chrome(options=options)
page=ChromiumPage()


start_url="https://novel.naver.com/webnovel/finish?"
filename="Novel_naver222.csv"

def korean_to_numeric(korean_number):
    # Strip any commas and remove the '만' character
    korean_number = korean_number.replace(',', '').replace('만', '')
    
    # Convert to float and adjust for '만' (10,000)
    if '.' in korean_number:
        numeric_value = float(korean_number)
    else:
        numeric_value = int(korean_number)
    
    return numeric_value / 10**4
for pg in range(46,52):
    print("PAGE:",pg)
    # driver.get(start_url+"&pg="+str(pg+1))
    page.get(start_url+"page="+str(pg+1))
    print(start_url+"page="+str(pg+1))
    
    soup=BeautifulSoup(page.html,'lxml')
    book_eles = soup.select(".card_list li")
    # author=soup.select_one('.author').text.split()
    # ranks = soup.select("span.zg-bdg-text")
    print(len(book_eles))
    i = 0
    for ele in book_eles:
        i += 1
        print(i)
        author=ele.select_one('.author').text.strip("[]'")
        r=ele.select_one('.score_area').text.replace('별점', '')

        # if i<=30 or i>=39:
        #     continue
        book_link = "https://novel.naver.com/" + ele.select_one(".item a")['href']
        print(book_link)
        page.get(book_link)
        print(book_link)
        time.sleep(1.5)
        print('scrolling')
        # driver.execute_script("window.scrollTo(0, window.scrollY+6000)")
        time.sleep(1.5)
        # soup2=BeautifulSoup(driver.page_source,'lxml')
        soup2=BeautifulSoup(page.html,'lxml')
        # soup2 = BeautifulSoup(html, 'html.parser')
        title=soup2.select_one("h2").text
        print(title)
        Author=soup2.select_one('.info_group > span:first-child').text.strip()
        # Tags=soup2.select(".tag_collection a")
        # tag_elements = soup.select('.tag_collection a')
        # tag_elements = soup.find_all(class_='tag_collection')
        # tag_elements = soup.select_one('.tag_collection > a')

        # tag_elements = soup.select('.tag_collection > a')
        tag_elements = soup2.select('.tag_collection a')

        # Extract the text from each element and join with '-'
        tag_text_list = [tag.text.strip('# ').strip() for tag in tag_elements]
        joined_tags = '-'.join(tag_text_list)
        # Iterate through each <a> tag and print its text content
        


        # Extract tags
        # Tags = '-'.join(tag.text.strip() for tag in tag_elements)
        url=book_link
        print(url)
        # introduction=soup2.select("#summaryText").text
#         summary_element = soup.select_one(".summary")

# # Check if summary_element exists before accessing its text
#         if summary_element:
#             introduction = summary_element.text.strip()  # Extract text and strip any leading/trailing whitespace
#             print(f"Introduction: {introduction}")
#         else:
#             print("Summary element not found")
        try:
            summary = soup2.select_one(".summary").text
        except:
            try:
                summary=soup2.select_one(".info_bottom p").text
            except:
                try:
                    summary=soup2.select_one("#summaryText").text
                except:
                    summary="NA"








        # Downloads=soup.select_one("span.count").text.strip()
        # print(Downloads)
        # Downloads = soup2.select_one('.info_group span.count').text.replace('만','000')
        # downloads_number = int(Downloads.replace(',', ''))  # Convert to integer after removing commas
        # formatted_downloads = '{:,}'.format(downloads_number)
        # downloads_text = soup2.select_one('.info_group span.count').text.strip()

        # # Clean up the text to extract just the numeric part
        # numeric_part = downloads_text.split()[1]  # Assuming the numeric part is the second part after splitting

        # # Replace '만' with '000' to handle Korean numeric suffix
        # numeric_part_cleaned = numeric_part.replace('만', '000')

        # # Remove commas and convert to integer
        # formatted_downloads = int(numeric_part_cleaned.replace(',', ''))
        try:
            downloads_text = soup2.select_one('.info_group span.count').text.strip()
            parts = downloads_text.split()  # Split by whitespace

            numeric_value = 0  # Initialize a variable to accumulate the numeric value

            for part in parts:
                if '억' in part:
                    # Extract the number before '억'
                    number_part = part.replace('억', '')
                    # Convert to integer and multiply by 100 million
                    numeric_value += int(number_part.replace(',', '')) * 100000000
                elif '만' in part:
                    # Extract the number before '만'
                    number_part = part.replace('만', '')
                    # Convert to integer and multiply by 10,000
                    numeric_value += int(number_part.replace(',', '')) * 10000
                else:
                    try:
                        # Attempt to convert the part to integer
                        numeric_value += int(part.replace(',', ''))
                    except ValueError:
                        # Handle cases where part cannot be converted to integer (e.g., '다운로드' or other non-numeric text)
                        continue
        except:
            numeric_value="NA"

# Clean up the text to extract just the numeric part
        
                        

# Format with commas
        # .text.strip().replace('만', '0000')
    #     if count_element:
    # # Extract text from the span element
    #         count_text = count_element.text.strip().replace('만', '0000')

            # Split the text to extract the Korean number
            # if '만' in count_text:
            #     korean_number = count_text.split(' ')[1].replace('만', '0000')  # Replace '만' with '0000' for million conversion
            # else:
            #     korean_number = None  # Handle case where '만' is not found
        # Downloads=count_element
        # Ratings=soup2.select(".score_area font font")
        # print(Ratings)
        score_element = soup.select_one('span.score_area')

        # Check if score_element exists before accessing its contents
        if score_element:
            # Extract text from the <span> element
            score_text = score_element.text.strip()
            
            # Extract the score (9.91)
            Ratings = score_text.split('별점')[-1].strip()
        LikesCount=soup2.select_one(".u_likeit_module .u_cnt").text.replace(',', '').strip()
        print(LikesCount)
        InterestsCount=soup2.select_one("#concernCount").text.strip().replace('만', '0000')
        print(InterestsCount)
        try:
            CommnetsCount=soup2.select_one(".u_cbox_count").text.replace(',', '').strip()
        except:
            CommnetsCount="NA"
        try:
            no_of_episodes_link=soup2.select_one(".end_lk_series a")['href']
        except:
            no_of_episodes="NA"
            pass
        if no_of_episodes_link:
            page.get(no_of_episodes_link)
            time.sleep(1.5)
            soup3=BeautifulSoup(page.html,'lxml')
            no_of_episodes=soup3.select_one("h5.end_total_episode strong").text.strip()
        else:
            no_of_episodes="NA"
            pass

        data = {
            "Title":title,
            "Author": author,
            "Tags": joined_tags,
            "URL":url,
            "Introduction":summary,
            "Total chapters":no_of_episodes,
            "Downloads": numeric_value,
            "Ratings":r,
            "Likes Count":LikesCount,
            "Interests Count":InterestsCount,
            "Comment Count":CommnetsCount,
            
        }
        # print(data)
        # break
        append_list_as_row(data)

page.close()   


