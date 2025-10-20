# Personal Library

## Description
This application allows the user to search for any book available in the Google Books API and store it within their personal library. The person will be able to see all the books that have been saved, and a random book is selected and recommended on a daily basis, having the possibility to add it to the collection as well. Each element (book) taken from the API has a determined level of visibility:
* ALL_PAGES > The entire book is available to read for free.
* PARTIAL > Only the first pages can be read, to read the rest, the user has to buy the book.
* NO_PAGES > No pages are available to read, either free or paying.

## Run the application
This project uses Docker to successfully install all the dependencies and required packages. You will find the mandatory configuration files in the repository (docker-compose.yml, Dockerfile, requirements.txt). Makefile contains an abbreviation of some useful commands to test and configure the application. Following statement stands for 'docker-compose up', which starts the program on localhost:8000.
* make up

## Scheduled task - To recommend one book per day
* It is configured to run every 5 minutes in order to see the functionality, but the intention in a production environment would be to have one book recommended every 24 hours.
* To edit the task configuration, you can use the admin panel provided by Django, first creating the superuser (make superuser) and then going to Crontabs.
