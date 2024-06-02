import asyncio
from pyppeteer import launch
import csv

async def scrape_indeed():
    
    # Browser instance is launched
    browser = await launch(executablePath='C:\Program Files\Google\Chrome\Application\chrome.exe', headless=False)  
    page = await browser.newPage()
    
    # Visit the site indeed.com
    await page.goto('https://www.indeed.com')
    
    # Waits for input field elements to load 
    await page.waitForSelector('#text-input-what')
    await page.waitForSelector('#text-input-where')
    
    # Type the search terms; Devops Engoneer and New York
    await page.type('#text-input-what', 'Devops Engineer')
    await page.type('#text-input-where', 'New York')
    
    # Click the search button
    await page.click('button[type="submit"]')
    
    # Waiting for next page to load
    await page.waitForNavigation()
    
    job_listings = await page.querySelectorAll('.resultContent')
    jobs = []

    for job in job_listings:
        # Extract the job title
        title_element = await job.querySelector('h2.jobTitle span[title]')
        title = await page.evaluate('(element) => element.textContent', title_element)

        # Extract the company name
        company_element = await job.querySelector('div.company_location [data-testid="company-name"]')
        company = await page.evaluate('(element) => element.textContent', company_element)

        # Extract the location
        location_element = await job.querySelector('div.company_location [data-testid="text-location"]')
        location = await page.evaluate('(element) => element.textContent', location_element)

        jobs.append({'title': title, 'company': company, 'location': location})
    
    await browser.close()
    
    # Save to CSV
    with open('scrapped.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Company', 'Location'])
        for job in jobs:
            writer.writerow([job['title'], job['company'], job['location']])
    
    print(f"Scraped {len(jobs)} jobs.")

# Run the coroutine
if __name__ == '__main__':
    asyncio.run(scrape_indeed())
