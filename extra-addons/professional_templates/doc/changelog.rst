.. _changelog:

Changelog
=========


`Version 1.6 (2017 DEC 05  14:35)`
------------------------------------------------
- Whats new?:
    - Small change to make the `watermark PDF` and `last page PDF` multi-company. Depending on the company of the user/salesperson, the document you print will bear the watermark of the company of the user printing the document. Same applies to the last page PDF. 

`Version 1.5 (2017-07-27 01:45)`
------------------------------------------------
- Whats new?:
    - Watermark Expression : You can define your own text to be printed on the PDF as watermark. This is in addition to letterhead/watermark PDF upload feature introduced in previous version (1.4). Now you can have both a watermark text printed on the PDF and also use your own letterhead as background for your reports. These two feature are Optional. Please refer to the module documentation for details on how to use this feature. 
    - Last pages: You can add last page/pages to your printed report. You simply upload a PDF that has content that will be appended to the printed report. This feature is useful if you have content such as Terms & Conditions or some promotional content or even some products you are advertising that you want your customers to see.

  - Write a simple python expression to generate a watermark..e.g if you want to print the invoice status i.e 'PAID' or 'NOT PAID' as watermark, you can simple have an expression such as `watermark = doc.status`

  - Added some useful guidelines on how to use the watermark feature on the Settings page

  - Re-organized the report settings to be more easy, intuitive and appealing

  - Fixed few bugs reported by users.

`Version 1.4 (2017-06-13 13:25)`
------------------------------------------------
- Introduced watermark to the templates. Now you can upload your watermark PDF (Go to Settings--> Technical --> Reports --> reports and search for ``report_invoice``, ``sale_order``, ``purchase_order``, ``rfq``, ``report_picking`` or ``report_deliveryslip`` and click on `Advanced properties` to add your watermark PDF as background for your report) as the background for your reports. In the report style settings, enable `transparent Background` in order to see your watermark design in the background. 

`Version 1.3 (2017-05-17 03:25)`
------------------------------------------------
- Increased the number of templates per report from 4 to 10. Now each report has 10 templates to choose from, plus the default Odoo template  

`Version 1.2 (2017-04-28 22:56)`
------------------------------------------------
- Added Shipping Address to all the invoice templates. If Shipping Address is different from the Invoicing address, then shipping address will be displayed separately on the invoice.

`Version 1.1 (2017-04-20 17:58)`
------------------------------------------------
- Added a new footer section with more details such as company name and address, Bank details, footer logo and the tagline

- The Footer logo is optional and can be disabled from the reports style settings


`Version 1.0 (2017-01-06 02:09)` - Major release
------------------------------------------------
- NOTE: To upgrade to this major release, please uninstall the older version 0.X and do a fresh installation of this version 1.0

- You can now create as many Report styles as you want and save them for use in different situations or per partner

- You can now associate/assign a report style to each Odoo Partner(customer,vendor,company,etc)

- The Report style assigned to a Partner will be used to print the report

- If partner does not have a report style assigned, The is a default report style to use 

- Read the module description for details on how to configure and assign report styles

`Version 0.3 (2016-12-09 02:17)`
------------------------------
- Now it's possible to display product image on Invoice, Sales Order, Quote, Delivery Note and Picking Slip. This feature is enabled by default but you can disable it in report settings (Company Data Form).

`Version 0.2 (2016-11-1)`
------------------------
- Fixed the missing font-icons in the reports


`Version 0.1 (2016-10-26)`
-------------------------
- Added support for Odoo 10 community and Enterprise editions

