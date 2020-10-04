

# FILE KẾT QUẢ NẰM Ở LINK GOOGLE DRVIE NÀY: https://drive.google.com/drive/folders/1AT85juW_gIsopIRlu1ribXyi-z0-_0_J?usp=sharing
# Chi tiết có thể tham khảo tại github: https://github.com/Pxtri2156/CS336.L11.KHTN/blob/master/Crawler/Crawler.ipynb
#                           hoặc colab: https://colab.research.google.com/drive/1tXgMwN92e17eurlWyZsIowawrrsRnj6u?usp=sharing


import requests
from bs4 import BeautifulSoup
import os
import csv

def Craweler_Tuoi_Tre_Ngay(url):

  '''
  This function allow you to crawl title, time_public, news, abstract, content, image_link every articles in paper
  '''
  # Parser link of paper 
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")

  #Take titles in paper
  titles = soup.findAll('h3', class_='title-news')

  # Take link from titles 
  links = [link.find('a').attrs["href"] for link in titles]
  data = []
  for link in links:
      news = requests.get("https://tuoitre.vn" + link)
      soup = BeautifulSoup(news.content, "html.parser")
      try:
        title = soup.find("h1", class_="article-title").text
      except:
        title = ("https://tuoitre.vn" + link).split("/")[3].split(".")[0]
      try:
        time_public = soup.find("div", class_="date-time").text
      except:
        time_public = "Format web not similar pre_page"   # Một số trang web có định đặc biệt không giống với các trang web khác
      try:
        abstract = soup.find("h2", class_="sapo").text
      except:
        abstract = "Format web not similar pre-page "     
      try:
        body = soup.find("div", id="main-detail-body")
      except:
        body = "Format web not similar pre-page "
      try:
        content = body.findChildren("p", recursive=False)[0].text +      body.findChildren("p", recursive=False)[1].text
      except:
        content = "Not Exit"
      try:
        image = body.find("img").attrs["src"]
      except:
        image = "Format web not similar pre-page"
      print("Tiêu đề: " + title)
      print("Thời gian: " + time_public)
      print("Link bài viết: " +  "https://tuoitre.vn" + link)
      print("Mô tả: " + abstract)
      print("Nội dung: " + content)
      print("Ảnh minh họa: " + image)
      print("_________________________________________________________________________")
      data.append({
          'title': title,
          'time_public': time_public,
          'link': "https://tuoitre.vn" + link
      })
  return data



def Craweler_Thang(month, days_of_month):
  '''
  This function allow you to crawl data from paper in month 
  '''
  data = {}
  for day in range(1,days_of_month + 1):

    print("***************************" +  str(day) + "-" + str(month) + "-2020" + "***********************************")
    # https://tuoitre.vn/xem-theo-ngay/1-9-2020.html
    paper_n = 1
    data_day = []
    while(1):
      #https://tuoitre.vn/timeline-xem-theo-ngay/0/1-9-2020/trang-1.htm
      link_url = "https://tuoitre.vn/timeline-xem-theo-ngay/0/" + str(day) + "-" + str(month) + "-2020/trang-" + str(paper_n) + ".htm"
      data_temp = Craweler_Tuoi_Tre_Ngay(link_url)
      if data_temp != []:  # Check page exit
        data_day = data_day + data_temp
        paper_n += 1
      else:
        break # End page of news
    time = str(day) + "-9-2020"
    data[time] = data_day 
    
  return data

def main():

  # Enter link 
  # Crawl data from Tuoi Tre News
  days_of_month = [31,28,31,30,31,30,31,31,30,31,30,31]
  # Enter month which you want to crawl 
  month = int(input("Enter month"))
  data = Craweler_Thang(month,days_of_month[month-1])
  #print('All article in Septemper ', data)

  # Save data to file
  # Đương dẫn file có thể thay đổi để có thể crawl dữ liệu về thành công 
  # Ở đây em dùng colab nên đường dẫn file nằm ở drive 
  with open('/content/drive/My Drive/My_Data/Data_crawl_from_Tuoi_Tre/data.csv', 'w', newline='') as file:
    fieldnames = ["title", "time_public","link"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for day in data.keys():
      for i in range(len(data[day])):
        writer.writerow(data[day][i])

if __name__ == "__main__":
    main()

