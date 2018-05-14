# Use CircleCI
FROM circleci/python:3.6-jessie

# Set maintainer.
MAINTAINER Mattia Ciollaro <mattia.ciollaro@spreemo.com>

# Install required dependencies for Python
RUN sudo pip install flake8
RUN sudo pip install gitpython

# Install R
RUN sudo sh -c 'echo "deb http://cloud.r-project.org/bin/linux/debian jessie-cran35/" >> /etc/apt/sources.list'
RUN sudo apt-key adv --keyserver keys.gnupg.net --recv-key 'E19F5F87128899B192B1A2C2AD5F960A256A04AF'
RUN sudo apt-get update
RUN sudo apt-get install r-base

# Install required dependencies for R
RUN sudo R -e "install.packages('lintr', repos='https://cloud.r-project.org')"

# Install npm and markdownlint-cli
RUN sudo apt-get update
RUN sudo apt-get install npm
RUN sudo npm install -g n
RUN sudo n 0.12.7
RUN sudo npm install -g markdownlint-cli

CMD ["python3"]
