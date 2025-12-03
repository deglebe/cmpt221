.. _`Troubleshooting`:

Troubleshooting
===============
This section describes some common issues that can arise and possible solutions.

Issue #1: Conflicting Port Usage with Docker
---------------------------------------------
When running Docker containers, you may encounter port conflicts if a port is already in use by another service or container. This commonly occurs when trying to start a PostgreSQL or Flask container on a port that's already occupied.

**Solution**: Dynamically provide a port to Docker by specifying a different port mapping in your ``docker-compose.yml`` file or when running the container. For example, instead of using the default PostgreSQL port 5432, you can map it to a different host port:

.. code-block:: yaml

    ports:
      - "5433:5432"  # Maps host port 5433 to container port 5432

This allows you to run multiple database instances or avoid conflicts with locally installed PostgreSQL services.

Issue #2: psycopg2 Installation Errors
---------------------------------------
The ``psycopg2-binary`` package may fail to install when included in ``requirements.txt``, especially on certain operating systems or when dependencies are not properly configured. This can prevent database connectivity from working correctly.

**Solution**: Install ``psycopg2-binary`` separately outside of the requirements file before installing other dependencies:

.. code-block:: text

    $ pip install psycopg2-binary
    $ pip install -r requirements.txt

This ensures that the PostgreSQL adapter is properly installed with all its system-level dependencies before other packages attempt to use it.

Issue #3: Local PostgreSQL vs Docker for Database Setup
-------------------------------------------------------
Setting up and managing a local PostgreSQL installation can be time-consuming and may cause conflicts with system configurations, especially when working across different operating systems or when multiple projects require different database versions.

**Solution**: Using Docker to spin up databases is more convenient and portable. Docker containers provide isolated database instances that can be easily started, stopped, and removed without affecting your local system. With ``docker-compose.yml``, you can define your database configuration once and share it across different environments. This approach eliminates the need for manual PostgreSQL installation, configuration, and maintenance, making it ideal for development workflows.
