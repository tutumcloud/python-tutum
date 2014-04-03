python-tutum
============

Python library for Tutum's API. Full documentation available at `http://docs.tutum.co/reference/api/ <http://docs.tutum.co/reference/api/>`_


Installing the library
^^^^^^^^^^^^^^^^^^^^^^

In order to install the Tutum Python library, you can use ``pip install``:

.. sourcecode:: bash

    pip install python-tutum

It will install a Python module called ``tutum`` which you can use to interface with the API.


Authorization
-------------

In order to be able to make requests to the API, you should first obtain an ApiKey for your account.
For this, log into Tutum, click on the menu on the upper right corner of the screen, and select **Get Api Key**

You can use your ApiKey with the Python library in any of the following ways (will be used in this order):

* Set the environment variables ``TUTUM_USER`` and ``TUTUM_APIKEY``:

.. sourcecode:: bash

    export TUTUM_USER=username
    export TUTUM_APIKEY=apikey

* Manually set it in your Python initialization code:

.. sourcecode:: python

    import tutum
    tutum.user = "username"
    tutum.apikey = "apikey"


Errors
------

Errors in the HTTP API will be returned with status codes in the 4xx and 5xx ranges.

The Python library will detect this status codes and raise ``TutumApiError`` exceptions with the error message,
which should be handled by the calling application accordingly.


Quick examples
--------------

Applications
^^^^^^^^^^^^

.. sourcecode:: python

    >>> import tutum
    >>> tutum.Application.list()
    [<tutum.api.application.Application object at 0x10701ca90>, <tutum.api.application.Application object at 0x10701ca91>]
    >>> tutum.Application.fetch("fee900c6-97da-46b3-a21c-e2b50ed07015")
    <tutum.api.application.Application object at 0x106c45c10>
    >>> app.name
    "my-python-app"
    >>> app = tutum.Application.create(image="tutum/hello-world", name="my-new-app", target_num_containers=2, container_size="XS")
    >>> app.save()
    True
    >>> app.target_num_containers = 3
    >>> app.save()
    True
    >>> app.stop()
    True
    >>> app.start()
    True
    >>> app.delete()
    True


Containers
^^^^^^^^^^

.. sourcecode:: python

    >>> import tutum
    >>> tutum.Container.list()
    [<tutum.api.container.Container object at 0x10701ca90>, <tutum.api.container.Container object at 0x10701ca91>]
    >>> tutum.Container.fetch("7d6696b7-fbaf-471d-8e6b-ce7052586c24")
    <tutum.api.container.Container object at 0x10701ca90>
    >>> container.web_public_dns = "my-web-app.example.com"
    >>> container.save()
    True
    >>> container.stop()
    True
    >>> container.start()
    True
    >>> container.logs
    "2014-03-24 23:58:08,973 CRIT Supervisor running as root (no user in config file)\n2014-03-24 23:58:08,973 WARN Included extra file \"/etc/supervisor/conf.d/supervisord-apache2.conf\" during parsing"
    >>> container.delete()
    True


Roles
^^^^^

.. sourcecode:: python

    >>> import tutum
    >>> tutum.Role.list()
    [<tutum.api.role.Role object at 0x10701ca90>]
    >>> tutum.Role.fetch("global")
    <tutum.api.role.Role object at 0x10701ca90>