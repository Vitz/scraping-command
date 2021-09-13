# Requirement

`pip install beautifulsoup4 
`  
`pip install requests-html`

# Use
Type command:
`python main.py`  
as default parameters will be used:   
`website = "https://www.searchenginejournal.com"  `   
`keywords_file = "keywords.txt"`  
  
Or type in console:  
`python main.py https://www.searchenginejournal.com keywords.txt
` 
You can still skip 'keywords.txt'.
  
As result, you are going to receive two file:  
- total.csv - the csv file contains keywords with total number of results,
- urls.csv - the csv file with every url collected from Google Search. 

# How it works
The program uses the Scraper class, which loops over given keywords and collects website links from google search service.
Links are collecting only if exist in given domain (directly connected with given website). 

# Future
A good point would be to add a random useragent generator and allow the use a proxy.
