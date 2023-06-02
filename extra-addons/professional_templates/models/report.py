# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://opensource.org/licenses/LGPL-3.0).
#
#This software and associated files (the "Software") may only be used (executed,
#modified, executed after modifications) if you have purchased a valid license
#from the authors, typically via Odoo Apps, or if you have received a written
#agreement from the authors of the Software (see the COPYRIGHT section below).
#
#You may develop Odoo modules that use the Software as a library (typically
#by depending on it, importing it and using its resources), but without copying
#any source code or material from the Software. You may distribute those
#modules under the license of your choice, provided that this license is
#compatible with the terms of the Odoo Proprietary License (For example:
#LGPL, MIT, or proprietary licenses similar to this one).
#
#It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#or modified copies of the Software.
#
#The above copyright notice and this permission notice must be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#DEALINGS IN THE SOFTWARE.
#
#########COPYRIGHT#####
# © 2017 Bernard K Too<bernard.too@optima.co.ke>
from base64 import b64decode
from logging import getLogger
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.utils import PdfReadError
from PIL import Image
from StringIO import StringIO
from odoo import api, models, _
logger = getLogger(__name__)

class Report(models.Model):
    _inherit = 'report'

    @api.model
    def get_pdf(self, docids, report_name, html=None, data=None):
        result = super(Report, self).get_pdf(docids, report_name, html=html, data=data)
        report = self._get_report_from_name(report_name)
        # watermark & last page uploaded at report level will override the one uploaded at company level
        watermark = report.pdf_watermark or self.env.user.company_id.pdf_watermark or None
        last_page = report.pdf_last_page or self.env.user.company_id.pdf_last_page or None
        if watermark:
            watermark = b64decode(watermark)
        if last_page:
            last_page = b64decode(last_page)
        if not watermark and not last_page: 
            return result

        pdf = PdfFileWriter()
        pdf_watermark = None
        if watermark:
            try:
                pdf_watermark = PdfFileReader(StringIO(watermark))
            except PdfReadError:
                try:
                    image = Image.open(StringIO(watermark))
                    pdf_buffer = StringIO()
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    resolution = image.info.get('dpi', report.paperformat_id.dpi or 90)
                    if isinstance(resolution, tuple):
                        resolution = resolution[0]
                    image.save(pdf_buffer, 'pdf', resolution=resolution) ##save the image as PDF 
                    pdf_watermark = PdfFileReader(pdf_buffer)
                except:
                    msg = _("Failed to load the non PDF watermark...")
                    logger.exception(msg)
            if not pdf_watermark:
                msg = _("No usable watermark found, got ")
                logger.info( msg + ' %s', watermark[:100])

        if pdf_watermark and pdf_watermark.numPages < 1:
            msg = _("Your watermark pdf does not contain any pages")
            logger.info(msg)
        if pdf_watermark and pdf_watermark.numPages > 1:
            msg = _("Your watermark pdf contains more than one page. All other pages will be ignored except the first page.")
            logger.info(msg)
        doc = PdfFileReader(StringIO(result))
        if pdf_watermark:
            for page in doc.pages:
                watermark_page = pdf.addBlankPage(page.mediaBox.getWidth(), page.mediaBox.getHeight())
                watermark_page.mergePage(pdf_watermark.getPage(0))
                watermark_page.mergePage(page)
        if last_page:
            pdf_last_page = PdfFileReader(StringIO(last_page))
            if pdf_watermark:
                for last in pdf_last_page.pages:
                    pdf.addPage(last)
            else:
                for page in doc.pages:
                    pdf.addPage(page)
                for last in pdf_last_page.pages:
                    pdf.addPage(last)

        pdf_content = StringIO()
        pdf.write(pdf_content)

        return pdf_content.getvalue()
