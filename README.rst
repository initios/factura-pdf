FACTURA PDF
===========

Create PDF invoice according to Spanish regulations.


Usage
_____
Check tests/tests_functional.py and facturapdf/strategies files.

==========
Generators
==========
To ease the creation of pdf flowables you can use the generators functions.

Element generator
-----------------
Creates a flowable based on a given string. Check the element function
to see the available elements. Arguments are given inside brackets separated by commas.

.. code-block:: python

    # Generates a Image flowable with 25 mm of width
    generators.element('image[logo.jpg,25]')

    # Generates a FrameBreak flowable
    generators.element('framebreak')

Chapter generator
-----------------
Creates a list of flowables passing any number of string arguments.

.. code-block:: python

    generators.chapter('Paragraph[Cat in the hat]', 'image[hat.jpg,25]')

    # Passing a string that is not a valid flowable keyword or anything that is not a string will do nothing
    # So you can mix chapter generator with another one at once
    generators.chapter('hello', [1, 2, 3]) # will return ['hello', [1, 2, 3]]

Testing
-------

.. code-block:: shell-session

    $ python -m unittest discover tests/


Check for output files at ``tests/output`` folder.

License
-------

BSD 3-Clause License. See LICENSE file.
