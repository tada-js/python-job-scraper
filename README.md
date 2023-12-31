# 파이썬 스크래퍼

## 원티드 스크래퍼

### 결과

#### 동작

![](https://velog.velcdn.com/images/nu11/post/a45c5106-9c4d-427a-a2f2-eef21787d0d2/image.gif)

#### wanted_jobs.csv

![](https://velog.velcdn.com/images/nu11/post/93819f8f-d34b-44f7-bc5b-ac0152d85f5b/image.png)

<br /><br />

### 동작 순서

1. chromium 실행
   (절차 확인을 위해 `headless=False` 지정)
2. 원티드 페이지로 이동
3. `searchButton` 검색 버튼 클릭
4. input placeholder 속성을 찾은 후 "프론트엔드" 입력
5. 엔터키 입력
6. 포지션 탭 클릭(이동)
7. End키를 사용한 5번의 스크롤
8. 서버로부터 응답받은 HTML을 BeautifulSoup 통해 파싱하여 content에 담기
9. 반복문으로 순회하며 각각의 공고(JobCard)들을 딕셔너리 형태로 먼저 저장한 뒤, 배열에 저장
10. wanted_jobs.csv 파일 생성(열기)
11. 첫 번째 row에 컬럼 작성
    ("Title", "Company", "Location", "Reward", "Link")
12. 반복문으로 순회하며 딕셔너리의 값들만 작성
13. 종료

### 해당 코드

```python
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import csv

p = sync_playwright().start()
browser = p.chromium.launch(headless=False)
page = browser.new_page()

page.goto("https://www.wanted.co.kr/jobsfeed")
time.sleep(2)
page.click("button.Aside_searchButton__Xhqq3")
time.sleep(2)
page.get_by_placeholder("검색어를 입력해 주세요.").fill('프론트엔드')
time.sleep(2)
page.keyboard.down("Enter")
time.sleep(3)
page.click("a#search_tab_position")
time.sleep(3)

# 페이지 스크롤
for x in range(5):
  page.keyboard.down("End")
  time.sleep(3)

content = page.content()
p.stop()

soup = BeautifulSoup(content, "html.parser")
jobs = soup.find_all("div", class_="JobCard_container__FqChn")

jobs_db = []

for job in jobs:
  link = f"https://www.wanted.co.kr/{job.find('a')['href']}"
  title = job.find("strong", class_="JobCard_title__ddkwM").text
  company_name = job.find("span", class_="JobCard_companyName__vZMqJ").text
  location = job.find("span", class_="JobCard_location__2EOr5").text
  reward = job.find("span", class_="JobCard_reward__sdyHn").text
  job = {
    "title": title,
    "company_name": company_name,
    "location": location,
    "reward": reward,
    "link": link
  }
  jobs_db.append(job)

file = open("wanted_jobs.csv", "w")
writer = csv.writer(file)
writer.writerow(["Title", "Company", "Location", "Reward", "Link"])

for job in jobs_db:
  writer.writerow(job.values())
```
