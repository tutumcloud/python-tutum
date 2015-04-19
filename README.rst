python-tutum
============

Python library for Tutum's API. Full documentation available at `https://docs.tutum.co/v2/api/?python <https://docs.tutum.co/v2/api/?python>`_


Installing the library
----------------------

In order to install the Tutum Python library, you can use ``pip install``:

.. sourcecode:: bash

    pip install python-tutum

It will install a Python module called ``tutum`` which you can use to interface with the API.


Authorization
-------------

In order to be able to make requests to the API, you should first obtain an ApiKey for your account.
For this, log into Tutum, click on the menu on the upper right corner of the screen, and select **Get Api Key**

You can use your ApiKey with the Python library in any of the following ways (will be used in this order):

* Manually set it in your Python initialization code:

.. sourcecode:: python

    import tutum
    tutum.user = "username"
    tutum.apikey = "apikey"

* Store it in a configuration file in ``~/.tutum``:

.. sourcecode:: ini

    [auth]
    user = "username"
    apikey = "apikey"

* Set the environment variables ``TUTUM_USER`` and ``TUTUM_APIKEY``:

.. sourcecode:: bash

    export TUTUM_USER=username
    export TUTUM_APIKEY=apikey


Errors
------

Errors in the HTTP API will be returned with status codes in the 4xx and 5xx ranges.

The Python library will detect this status codes and raise ``TutumApiError`` exceptions with the error message,
which should be handled by the calling application accordingly.


Quick examples
--------------

Services
^^^^^^^^^^^^

.. sourcecode:: python

    >>> import tutum
    >>> tutum.Service.list()
    [<tutum.api.service.Service object at 0x10701ca90>, <tutum.api.service.Service object at 0x10701ca91>]
    >>> service = tutum.Service.fetch("fee900c6-97da-46b3-a21c-e2b50ed07015")
    <tutum.api.service.Service object at 0x106c45c10>
    >>> service.name
    "my-python-app"
    >>> service = tutum.Service.create(image="tutum/hello-world", name="my-new-app", target_num_containers=2)
    >>> service.save()
    True
    >>> service.target_num_containers = 3
    >>> service.save()
    True
    >>> service.stop()
    True
    >>> service.start()
    True
    >>> service.delete()
    True


Containers
^^^^^^^^^^

.. sourcecode:: python

    >>> import tutum
    >>> tutum.Container.list()
    [<tutum.api.container.Container object at 0x10701ca90>, <tutum.api.container.Container object at 0x10701ca91>]
    >>> container = tutum.Container.fetch("7d6696b7-fbaf-471d-8e6b-ce7052586c24")
    <tutum.api.container.Container object at 0x10701ca90>
    >>> container.public_dns = "my-web-app.example.com"
    >>> container.save()
    True
    >>> container.stop()
    True
    >>> container.start()
    True
    >>> container.logs
    "2014-03-24 23:58:08,973 CRIT Supervisor running as root (no user in config file) [...]"
    >>> container.delete()
    True

