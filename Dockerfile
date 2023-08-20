FROM python:3.10

# Install Terraform
RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add - && \
    apt update --yes && \
    apt install software-properties-common --yes && \
    apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main" --yes && \
    apt update && apt install terraform --yes && \
    apt install npm && \
    npm install typescript -g

COPY . .

RUN pip install -r requirements.txt

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz

# Install firefox, geckodriver and put it on path
RUN apt install firefox --yes && \
    tar -xvzf geckodriver* && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin/
