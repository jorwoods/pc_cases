#! /usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR
cd proxies
terraform init
terraform apply --auto-approve
terraform output proxy_ips | grep -v EOT > ../proxy_ips.txt
sed -i 's/$/:8888/' ../proxy_ips.txt # Add port to the proxy outputs
sleep 60 # Wait a minute so the instances are available and ready to receive requests
cd ..
scrapy crawl newegg -O newegg_cases.json
rm proxy_ips.txt
cd proxies
terraform apply -destroy --auto-approve
cd $SCRIPT_DIR
