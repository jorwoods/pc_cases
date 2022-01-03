# PC Case

In the hunt for a PC case that fit in the
[uplift under desk mount](https://www.upliftdesk.com/cpu-holder-by-uplift-desk/)
it was difficult to find a case that fit the required dimensions, while also
able to fit a full size GPU. The solution? Scrape the websites of retailers,
process and filter the cases down to only those fitting the required dimensions
and then look through the resulting URLs.

# How to run

Replace the `...` with access key and secret key for your AWS keys.

```sh

docker run -e "AWS_ACCESS_KEY_ID=..." -e "AWS_SECRET_ACCESS_KEY=..." -it $(docker build -q .)
/bin/bash run.sh

```