===========================
Tracking Fields in Partners
===========================

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:d66d964ab6c40b97aa727924bac57e6c367ceb4f5564657dd09d0fb0c442cf27
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fcrm-lightgray.png?logo=github
    :target: https://github.com/OCA/crm/tree/17.0/marketing_crm_partner
    :alt: OCA/crm
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/crm-17-0/crm-17-0-marketing_crm_partner
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/crm&target_branch=17.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

This module extends the functionality of the CRM to support having the
tracking fields available in the partner and copy them there
automatically when the partner is created from a lead/opportunity.

**Table of contents**

.. contents::
   :local:

Usage
=====

To use this module, here are the steps:

1.  If you don't have the "Leads" tab at the top menu in the crm app, go
    to **Settings > CRM** and check the box **Leads**. |crm settings|
2.  Go to **CRM > Leads > Create**.
3.  Fill the required fields.
4.  Go to **Extra Info > Marketing** and fill those fields: |lead view|
5.  **Save**.
6.  Click **Convert to Opportunity**.
7.  Choose the option **Customer > Create a new customer**.
8.  Click **Create Opportunity**. |choose customer|
9.  Click on the name of the newly linked partner. |new linked partner|
10. Go to tab **Sales & Purchases**.
11. There you have the new fulfilled fields in the marketing section.
    |partner marketing|

.. |crm settings| image:: https://raw.githubusercontent.com/OCA/crm/17.0/marketing_crm_partner/static/description/crm_settings.png
.. |lead view| image:: https://raw.githubusercontent.com/OCA/crm/17.0/marketing_crm_partner/static/description/lead_marketing.png
.. |choose customer| image:: https://raw.githubusercontent.com/OCA/crm/17.0/marketing_crm_partner/static/description/convert_to_opportunity.png
.. |new linked partner| image:: https://raw.githubusercontent.com/OCA/crm/17.0/marketing_crm_partner/static/description/new_linked_partner.png
.. |partner marketing| image:: https://raw.githubusercontent.com/OCA/crm/17.0/marketing_crm_partner/static/description/marketing_fields.png

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/crm/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/crm/issues/new?body=module:%20marketing_crm_partner%0Aversion:%2017.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
-------

* Tecnativa

Contributors
------------

-  `Tecnativa <https://www.tecnativa.com>`__:

   -  Rafael Blasco <rafael.blasco@tecnativa.com>
   -  Jairo Llopis <jairo.llopis@tecnativa.com>
   -  Vicent Cubells <vicent.cubells@tecnativa.com>
   -  David Vidal <david.vidal@tecnativa.com>
   -  Cristina Martin R. <cristina.martin@tecnativa.com>
   -  Marcel Savegnago <marcel.savegnago@escodoo.com.br>
   -  Ahmet Yiğit Budak <yigit@altinkaya.com.tr>

Maintainers
-----------

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/crm <https://github.com/OCA/crm/tree/17.0/marketing_crm_partner>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
