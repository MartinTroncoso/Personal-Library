# Personal Library

## Description
This application allows the user to search for any book available in the Google Books API and store it within his/her personal library. The person will be able to see all the books that have been saved, and a random book is picked up and recommended on a daily basis, having the possibility to add it to the collection as well. Each element (book) taken from the API has a determined level of visibility:
* ALL_PAGES > The entire book is available for free to read.
* PARTIAL > Only the first pages can be read, to read the rest, the user has to buy the book.
* NO_PAGES > No pages available to read, neither free nor paying.

## Run the application
This project uses Docker to successfully install all the dependencies and required packages. You will find the mandatory configuration files in the repository (docker-compose.yml, Dockerfile, requirements.txt). Makefile contains an abbreviation of some useful commands to test and configure the application. Following statement stands for 'docker-compose up', which starts the program:
* make up
