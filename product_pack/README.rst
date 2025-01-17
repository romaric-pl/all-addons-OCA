============
Product Pack
============

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:6412314c32b470ebaa9ba73edd671e2513bf0b8c9faa4703dcb22faf76692670
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fproduct--pack-lightgray.png?logo=github
    :target: https://github.com/OCA/product-pack/tree/16.0/product_pack
    :alt: OCA/product-pack
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/product-pack-16-0/product-pack-16-0-product_pack
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/product-pack&target_branch=16.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

This module allows you to define a product as a *Product Pack*. Each
*Product Pack* has a list of products that are part of this pack.

**Table of contents**

.. contents::
   :local:

Usage
=====

To use this module, you need to:

#. Go to *Sales > Products > Products*, create a product and set "Is Pack?".
#. Set *Pack Type* and *Pack component price*.
#. Then choose the products to include in the pack.

`Product pack` is a base module for `sale_product_pack` and other modules that
needs to use packs. `Pack type` and `Pack component price` are used to define
the behavior that the packs will have when it is selected in the sales order
lines (if `sale_product_pack` module is installed).
The options of this field are the followings:

`Pack type`:

  * Detailed: It allows you to select an option defined in
    `Pack component price` field.
  * Non Detailed: Will not show the components information,
    only the pack product and the price will be the its price plus the sum of
    all the components prices.

`Pack component price`:

  * Detailed per component: will show each components and its prices,
    including the pack product itself with its price.
  * Totalized in main product: will show each component but will not show
    components prices. The pack product will be the only one that has price
    and this one will be its price plus the sum of all the components prices.
  * Ignored: will show each components but will not show
    components prices. The pack product will be the only one that has price
    and this one will be the price set in the pack product.

+-----------------------------+-----------------------------+---------------------------------+-----------------------------------------+----------------------+
| **Pack type**               | **Show components on SO?**  | **Sale price**                  | **Discount**                            | **Can be modified?** |
+=============================+=============================+=================================+=========================================+======================+
| **Detailed per components** | Yes, with their prices      | Components + Pack               | Applies to the price of the pack and    | Yes, configurable    |
|                             |                             |                                 | the components                          |                      |
+-----------------------------+-----------------------------+---------------------------------+-----------------------------------------+----------------------+
| **Detailed - Totalized**    | Yes, with their prices at 0 | Components                      | Applies to the total (pack + components)| No                   |
+-----------------------------+-----------------------------+---------------------------------+-----------------------------------------+----------------------+
| **Detailed - Ignored**      | Yes, with their prices at 0 | Only Pack                       | Applies to the pack                     | No                   |
+-----------------------------+-----------------------------+---------------------------------+-----------------------------------------+----------------------+
| **No detailed**             | No                          | Components                      | Applies to the total (pack + components)| No                   |
+-----------------------------+-----------------------------+---------------------------------+-----------------------------------------+----------------------+

**Note:** If pricelist enabled, Odoo will display the price according to the corresponding pricelist. In the case of a pricelist with discount policy "Show public price & discount to the customer" keep in mind that the "Non Detailed" and "Detailed - Totalized in main product" packs do not display the discount.

Known issues / Roadmap
======================

* It could add another *Pack Type* called maybe *merged* in *Packs*, in which
  the calculation of the related sale order line *Unit Price* is equal to
  *main product Pack price* + *sum of all its component*
* Make *product.pack.line* multi-company

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/product-pack/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/product-pack/issues/new?body=module:%20product_pack%0Aversion:%2016.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* NaN·tic
* ADHOC SA
* Tecnativa

Contributors
~~~~~~~~~~~~

* `ADHOC SA <https://www.adhoc.com.ar>`_:

  * Juan José Scarafía
  * Nicolas Mac Rouillon
  * Katherine Zaoral
  * Bruno Zanotti
  * Augusto Weiss
  * Nicolas Col
* `NaN·TIC <http://www.nan-tic.com>`_
* `Tecnativa <https://www.tecnativa.com>`_:

  * Ernesto Tejeda
  * Pedro M. Baeza
  * Jairo Llopis
  * Sergio Teruel
* `Sygel <https://www.sygel.es>`_:

  * Manuel Regidor

* `Acsone <https://www.acsone.eu/>`_:

  * Maxime Franco

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

.. |maintainer-ernestotejeda| image:: https://github.com/ernestotejeda.png?size=40px
    :target: https://github.com/ernestotejeda
    :alt: ernestotejeda

Current `maintainer <https://odoo-community.org/page/maintainer-role>`__:

|maintainer-ernestotejeda| 

This module is part of the `OCA/product-pack <https://github.com/OCA/product-pack/tree/16.0/product_pack>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
