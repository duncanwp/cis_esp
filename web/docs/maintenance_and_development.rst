Maintenance and Development
===========================

Design
------

As far as possible the platfrom uses a standard Django MVC design. We use the Djagngo-Rest-Framework (DRF) to create
an API for the underlying data which the various views should use directly. We use Leaflet for the map components
(linked to Mapbox for the basemap).

A high level story board:

.. image:: https://www.draw.io/?chrome=0&lightbox=1&edit=https%3A%2F%2Fwww.draw.io%2F%23DStory%2520board.html&nav=1#DStory%20board.html

An Entity Relationship Diagram (ERD) of the data model components:

.. image:: https://www.draw.io/?chrome=0&lightbox=1&edit=https%3A%2F%2Fwww.draw.io%2F%23DCIS_ESP_ERD&nav=1#DCIS_ESP_ERD

