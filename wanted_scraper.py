from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import csv

class JobScraper:
    def __init__(self, keyword):
        self.keyword = keyword
        self.jobs_db = []

    def scrape(self):
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.wanted.co.kr/jobsfeed")
        time.sleep(2)
        page.click("button.Aside_searchButton__Xhqq3")
        time.sleep(2)
        page.get_by_placeholder("검색어를 입력해 주세요.").fill(self.keyword)
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

        self._parse_content(content)

    def _parse_content(self, content):
        soup = BeautifulSoup(content, "html.parser")
        jobs = soup.find_all("div", class_="JobCard_container__FqChn")

        for job in jobs:
            link = f"https://www.wanted.co.kr/{job.find('a')['href']}"
            title = job.find("strong", class_="JobCard_title__ddkwM").text
            company_name = job.find("span", class_="JobCard_companyName__vZMqJ").text
            location = job.find("span", class_="JobCard_location__2EOr5").text
            reward = job.find("span", class_="JobCard_reward__sdyHn").text
            job_info = {
                "title": title,
                "company_name": company_name,
                "location": location,
                "reward": reward,
                "link": link
            }
            self.jobs_db.append(job_info)

    def save_to_csv(self):
        file = open(f"{self.keyword}_jobs.csv", "w")
        writer = csv.writer(file)
        writer.writerow(["Title", "Company", "Location", "Reward", "Link"])

        for job in self.jobs_db:
            writer.writerow(job.values())

        file.close()

# scraper = JobScraper('keyword')
scraper = JobScraper('프론트엔드')

scraper.scrape()
scraper.save_to_csv()
