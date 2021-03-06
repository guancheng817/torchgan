===============
torchgan.models
===============

.. currentmodule:: torchgan.models

This models subpackage is a collection of popular GAN architectures. It has
the support for existing architectures and provides a base class for
extending to any form of new architecture. Currently the following models
are supported:

.. contents::
    :local:

You can construct a new model by simply calling its constructor.

.. code:: python

    >>> import torchgan.models as models
    >>> dcgan_discriminator = DCGANDiscriminator()
    >>> dcgan_generator = DCGANGenerator()

All models follow the same structure. There are additional customization options.
Look into the individual documentation for such capabilities.

Vanilla GAN
===========

Generator
---------

.. autoclass:: Generator
    :members:

    .. automethod:: _weight_initializer

Discriminator
-------------

.. autoclass:: Discriminator
    :members:

    .. automethod:: _weight_initializer

Deep Convolutional GAN
======================

DCGANGenerator
--------------

.. autoclass:: DCGANGenerator
    :members:

DCGANDiscriminator
------------------

.. autoclass:: DCGANDiscriminator
    :members:

Conditional GAN
===============

ConditionalGANGenerator
-----------------------

.. autoclass:: ConditionalGANGenerator
    :members:

ConditionalGANDiscriminator
---------------------------

.. autoclass:: ConditionalGANDiscriminator
    :members:

InfoGAN
=======

InfoGANGenerator
----------------

.. autoclass:: InfoGANGenerator
    :members:

InfoGANDiscriminator
--------------------

.. autoclass:: InfoGANDiscriminator
    :members:

AutoEncoders
============

AutoEncodingGenerator
---------------------

.. autoclass:: AutoEncodingGenerator
    :members:

AutoEncodingDiscriminator
-------------------------

.. autoclass:: AutoEncodingDiscriminator
    :members:

Auxiliary Classifier GAN
========================

ACGANGenerator
--------------

.. autoclass:: ACGANGenerator
    :members:

ACGANDiscriminator
------------------

.. autoclass:: ACGANDiscriminator
    :members:
