
# Scrapping

 - is the act of programmatically retrieving / downloading a web page's data and extracting very specific information from it.
   - mine data, small-scale datasets
   - not illegal if data is publically available and you do not cause disruptions

### Crawling
 - act of programmatically retrieving / downloading a web page's data, extracting its hyperlinks and following them.
   - indexing pages

#### Advice
 - use api if available instead of scrapping.
 - respect robots.txt
 - use reasonable crawl rate / don't overload the site (10-15 sec delay)
 - identify your web scraper and link back to page in user-agent
 - do not publish scraped data

#### Operations
 - fetch
   - ( urllib / requests / httplib )
 - parse
   - ( beautifulsoup )

#### Application vs Library
 - Framework
   - defines hw your app works
   - framework invokes the code

   - scrapy
     - async
     - control over data flow
     - fault tolerant - if task fails, still can operate
     - reliable, speed, parallel exec.

 - Library
   - your app invokes the library

### URLS
 - https://github.com/scrapinghub/portia