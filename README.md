# PC Case

In the hunt for a PC case that fit in the
[uplift under desk mount](https://www.upliftdesk.com/cpu-holder-by-uplift-desk/)
it was difficult to find a case that fit the required dimensions, while also
able to fit a full size GPU. The solution? Scrape the websites of retailers,
process and filter the cases down to only those fitting the required dimensions
and then look through the resulting URLs.

# How to run

```sh

pipenv run scrapy crawl newegg -O newegg_cases.json
pipenv run python process_newegg_cases.py

```