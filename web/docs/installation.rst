Installation
============

Development
-----------

This should be straight-forward using the docker compose file. Having installed docker (and compose) Simply type::

  docker-compose build

followed by::

  docker-compose up -d

You can add test data by doing::

  docker exec -it <container> python /cis-esp/manage.py loaddata /cis-esp/test_fixtures.json

Or add a larger test set by copying the data in first::

  docker cp large_test_fixtures.json <container>:large_test_fixtures.json

To wipe the database type::

  docker volume rm pgdata


Production / Test
-----------------

This is the same as above except we point docker to the production compose script::

  docker-compose -f production.yml up -d

Ensure that the production `.env` file is in the project directory and ensure to check firewall access on port 80.
