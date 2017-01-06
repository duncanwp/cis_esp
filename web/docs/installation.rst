Installation
============

This should be straight-forward using the docker compose file. Having installed docker (and compose) Simply type::

  docker-compose build

followed by::

  docker-compose up -d

You can add test data by doing::

  docker exec -it <container> python /cis-esp/manage.py loaddata /cis-esp/test_fixtures.json

Or add a larger test set by copying the data in first::

  docker cp large_test_fixtures.json <container>:large_test_fixtures.json
