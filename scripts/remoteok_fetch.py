import requests
from bs4 import BeautifulSoup
import json

def fetch_remoteok_jobs():
    url = 'https://remoteok.com/remote-dev-jobs'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs_data = []

    jobs = soup.find_all('tr', class_='job')[:40]

    for job in jobs:
        try:
            title = job.find('h2', itemprop='title').get_text(strip=True)
            company = job.find('h3', itemprop='name').get_text(strip=True)
            link = 'https://remoteok.com' + job['data-href']
            tags = [tag.get_text(strip=True) for tag in job.find_all('div', class_='tag')]
            location_tag = job.find('div', class_='location')
            location = location_tag.get_text(strip=True) if location_tag else "Worldwide"
            date_tag = job.find('time')
            date_posted = date_tag['datetime'][:10] if date_tag else "Unknown"

            # Heuristic: Try to find salary or experience in tags
            salary = next((tag for tag in tags if '$' in tag or 'USD' in tag), "Not listed")
            experience_level = next((tag for tag in tags if tag.lower() in ['junior', 'senior', 'entry-level']), "Not listed")
            work_type = next((tag for tag in tags if tag.lower() in ['contract', 'full-time', 'part-time']), "Not listed")

            jobs_data.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Experience": experience_level,
                "Salary": salary,
                "Company URL": "Not Available",  # RemoteOK doesn't show
                "Apply URL": link,
                "Posted Date": date_posted,
                "Fields": tags,
                "Experience Level": experience_level,
                "Contract Type": work_type,
                "Work Type": work_type,
                "Apply Type": "Direct Link"
            })
        except Exception as e:
            print("❌ Error parsing a job listing:", e)

    return jobs_data


if __name__ == "__main__":
    jobs = fetch_remoteok_jobs()

    print(json.dumps(jobs, indent=2))

    with open("remoteok_jobs_detailed.json", "w", encoding='utf-8') as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Fetched {len(jobs)} jobs and saved to remoteok_jobs_detailed.json")
