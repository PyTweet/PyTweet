============
Contributing
============

Welcome to ``PyTweet``'s contributor's guide.

This document focuses on getting any potential contributor familiarized
with the development processes, but `other kinds of contributions` are also
appreciated.

Issue Reports
=============

If you experience bugs or general issues with ``pytweet``, please have a look
on the `issue tracker`. If you don't see anything useful there, please feel
free to open an issue report.


Documentation Improvements
==========================

You can help improve ``pytweet`` docs by making them more readable and coherent, or
by adding missing information and correcting mistakes.

``pytweet`` documentation uses Sphinx as its main documentation compiler.
This means that the docs are kept in the same repository as the project code, and
that any documentation update is done in the same way was a code contribution.
**NOTE**: PyTweet's docs uses reStructuredText

When working on documentation changes in your local machine, you can
compile them using the following commands:

.. code:: bash

    cd docs/
    make clean html
    python3 -m http.server -d _build/html



Code formatting
==================

This project (``PyTweet``) follows the black code-style with line-length as ``120``
You can use black easily by doing:

.. code:: bash

    pip install black
    black setup.py pytweet --line-length 120


If you want to see what changes black will make, you can do:

.. code:: bash

    pip install black
    black --diff setup.py pytweet --line-length 120



Commit Messages
==================

We use semantic commit messages. All commits must follow this, `Click here to find out how to write them. <https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716>`_

Testing
==================

Currently, we are setting up tests with pytest, however it is not done yet, don't put any tests folders, if you do please put the them in the ``.gitignore``



Code Contributions
==================

Create an environment
---------------------

Before you start coding, we recommend creating an isolated `virtual
environment` to avoid any problems with your installed Python packages.
This can easily be done via either virtualenv

.. code:: bash

    pip install virtualenv
    virtualenv venv
    source venv/bin/activate

Clone the repository
--------------------

#. Create an user account on the github if you do not already have one.
#. Fork the project repository: click on the *Fork* button near the top of the
   page. This creates a copy of the code under your account on github.
#. Clone this copy to your local disk::

    git clone https://github.com/YOUR_NAME/PyTweet
    cd pytweet

#. You should run::

    pip install -U pip setuptools -e .

Implement your changes
----------------------

#. Create a branch to hold your changes (Optional)::

    git checkout -b my-feature

   and start making changes.

#. Start your work on this branch. Don't forget to add docstrings to new
   functions, modules and classes, especially if they are part of public APIs.

#. When you’re done editing, do::

    git add --all
    git commit

Submit your contribution
------------------------

#. If everything works fine, push your local branch to github with::

    git push -u origin <my-feature>

#. Go to the web page of your fork and click the contrbuting button
   to send your changes for review.

      Find more detailed information `creating a PR`.
