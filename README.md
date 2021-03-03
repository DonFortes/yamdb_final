

# Project Title

The YaMDb project collects user reviews of works (Title). The works are divided into categories: "Books", "Movies", "Music". In each category there are works: books, movies or music. Grateful or outraged readers leave text reviews for the works and give the work a rating (rating in the range from one to ten). From the set of ratings, the average score of the product is automatically calculated.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing

1. Clone a repository
git clone https://github.com/DonFortes/infra_sp2

2. Launching the app
docker-compose up

3. Make migrations
docker-compose exec web python manage.py migrate

4. Copy static data
docker-compose exec web python manage.py collectstatic --noinput

5. Filling the database with initial data
docker-compose exec web python manage.py loaddata fixtures.json 

See this project on internet

API documentation is available at
http://178.154.253.131:8001/

Access to the admin panel
http://178.154.253.131:8001/admin

List of categories
http://178.154.253.131:8001/api/v1/categories/
List of genres
http://178.154.253.131:8001/api/v1/genres/
List of titles
http://178.154.253.131:8001/api/v1/titles/
Users
http://178.154.253.131:8001/api/v1/users/


https://github.com/DonFortes/yamdb_final/workflows/yamdb_workflow/badge.svg

![example workflow](https://github.com/DonFortes/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)
