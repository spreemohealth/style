# Use slim Python 3
FROM rocker/r-base

# Add maintainer
label maintainer="Mattia Ciollaro mattiaciollaro@gmail.com"

# Dependencies
RUN apt-get update
RUN apt-get install -y libssl-dev
RUN apt-get install -y libcurl4-openssl-dev

# Install Python 3 and pip
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# Install flake8
RUN pip3 install flake8

# Install lintr
RUN R -e "install.packages('lintr', repos='https://cloud.r-project.org')"

# Install markdownlint-cli
RUN apt-get install -y npm
RUN npm install -g markdownlint-cli

# Install git
RUN apt-get install -y git

# Create a directory where to mount git repo
RUN mkdir repo
RUN echo cd repo >> /root/.bashrc

# Shorten bash prompt
RUN echo export 'PS1="style> "' >> /root/.bashrc

# Clone the style repository but remove the .git subdirectory
RUN git clone https://github.com/mattiaciollaro/style.git
RUN rm -rf style/.git

# Copy entry point scripts
COPY start.sh /start.sh

ENTRYPOINT ["/bin/bash", "/start.sh"]
