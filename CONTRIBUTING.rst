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
free to fire an issue report.

New issue reports should include information about your programming environment
(e.g., operating system, Python version) and steps to reproduce the problem.
Please try also to simplify the reproduction steps to a very minimal example
that still illustrates the problem you are facing. By removing other factors,
you help us to identify the root cause of the issue.


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

.. code:: sh

cd docs/
make clean html
python3 -m http.server -d _build/html


Code Contributions
==================

Create an environment
---------------------

Before you start coding, we recommend creating an isolated `virtual
environment` to avoid any problems with your installed Python packages.
This can easily be done via either virtualenv

    pip install virtualenv
    virtualenv venv
    source venv/bin/activate

Clone the repository
--------------------

#. Create an user account on |the repository service| if you do not already have one.
#. Fork the project repository: click on the *Fork* button near the top of the
   page. This creates a copy of the code under your account on |the repository service|.
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

#. If everything works fine, push your local branch to |the repository service| with::

    git push -u origin <my-feature>

#. Go to the web page of your fork and click the contrbuting button
   to send your changes for review.

      Find more detailed information `creating a PR`.


Testing
------------------------

Currently we are setting up tests with pytest, however it is not done yet, don't put any tests folders, if you do please put the them in the ``.gitignore``
