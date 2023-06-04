#########################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-TODAY Probuse Consulting Service Pvt. Ltd. (<http://probuse.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################################

{
    'name' : 'Payroll Extend',
    'version': '1.0',
    'license': 'AGPL-3',
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'category' : 'Human Resources',
    'website': 'https://www.probuse.com',
    'description': ''' 
This module adds the email chatter in payslip and payslip batches form. Also displays the list of payslip and payslip-batches in descending order.
  ''',
    'depends':['hr_payroll'],
    'data' : [
              'payslip_view.xml'
              ],
    'installable':True,
    'auto_install':False

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
