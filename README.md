# Google Cloud Documentation Scraper

Create the `conda` environment:

```
conda env create -f environment.yml
```

Modify the `services` variable within the `gcpDocScraper.py` script to include one URI for each GCP service. 
URIs must include the side navbar.

Run the script:

```
python gcpDocScraper.py
```

Under `csvs`, there will be a number of semicolon-delimited CSV files that can be used to track reading.
Under `epubs`, there will be a number of `epub` files.
Under `html`, there will be a number of scraped `html` pages that include only the article content (minus the sidebar and all the other nonsense that Google clutters its pages with).
