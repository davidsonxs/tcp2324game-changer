import hockey_scraper

# Scrapes the 2015 & 2016 season with shifts and stores the data in a Csv file (both are equivalent!!!)
hockey_scraper.scrape_seasons([20], True)
hockey_scraper.scrape_seasons([2020], True, data_format='Csv')