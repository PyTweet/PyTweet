:orphan:

.. currentmodule:: pytweet

.. versionadded:: 1.2.0

Logging
===============

PyTweet now provides **logging** support!
However, you will not see these logs since they are muted.

To it up you can do

.. code:: py

    import logging

    logging.basicConfig(level=logging.INFO)

This will log everything being logged my pytweet!

More advanced logging setups are possible by logging them to a file.
You can do this like this

.. code:: py

    import logging

    logging.basicConfig(
        level=logging.INFO, 
        filename="pytweet.log", 
        filemode="w",
        encoding="utf-8",
        format="%(asctime)s:%(levelname)s:%(name)s: %(message)s",
        )
