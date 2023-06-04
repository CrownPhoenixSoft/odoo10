##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    user_ids = fields.Many2many(
        'res.users',
        'journal_security_journal_users',
        'journal_id',
        'user_id',
        # string='Restricted to Users',
        string='Totally restricted to',
        help='If choose some users, then this journal and the information'
        ' related to it will be only visible for those users.',
        copy=False,
    )

    modification_user_ids = fields.Many2many(
        'res.users',
        'journal_security_journal_modification_users',
        'journal_id',
        'user_id',
        string='Modifications restricted to',
        help='If choose some users, then only this users will be allow to '
        ' create, write or delete accounting data related of this journal. '
        'Information will still be visible for other users.',
        copy=False,
    )

    journal_restriction = fields.Selection(
        [('none', 'None'),
         ('modification', 'Modificacion'),
         ('total', 'Total')],
        string="Type of Restriction",
        compute='_compute_journal_restriction',
        readonly=False,
    )

    @api.depends()
    def _compute_journal_restriction(self):
        for rec in self:
            if rec.user_ids:
                rec.journal_restriction = 'total'
            elif rec.modification_user_ids:
                rec.journal_restriction = 'modification'
            else:
                rec.journal_restriction = 'none'

    @api.multi
    @api.constrains('user_ids')
    def check_restrict_users(self):
        self._check_journal_users_restriction('user_ids')

    @api.multi
    @api.constrains('modification_user_ids')
    def check_modification_users(self):
        self._check_journal_users_restriction('modification_user_ids')

    @api.multi
    def _check_journal_users_restriction(self, field):
        """
        This check seems to be necessary only for an odoo bug that does not
         would control the m2m fields
        """
        # esto es porque las ir rules tienen un cache que no permite
        # que el cambio aplique en el momento
        self.env['ir.rule'].clear_caches()

        if self.modification_user_ids and self.user_ids:
            raise ValidationError(_(
                'You cannot set values in Totally Restricted To: and'
                '"Modifications Restricted To:" simultaneously. these options are to be used exclusively '
                ))

        # con sudo porque ya no los ve si no se asigno
        env_user = self.env.user
        if env_user.id == SUPERUSER_ID:
            # if superadmin no need to check
            return True
        for rec in self.sudo():
            journal_users = rec[field]
            # journal_users = rec.user_ids
            if journal_users and env_user not in journal_users:
                raise ValidationError(_(
                    'You cannot restrict the journal "%s" to suers without '
                    'including yourself as you would stop seeing this '
                    'journal') % (rec.name))
        # necesitamos limpiar este cache para que no deje de verlo
        self.env.user.context_get.clear_cache(self)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """
        For users, users cannot choose journal where they cannot
         write, we modify the search function. We do not do it by rule of
         permission because if they can't see the journal ends up giving errors in
         any place that uses a field related to something in the journal

        """
        user = self.env.user
        # if superadmin, do not apply
        if user.id != 1:
            args += [
                '|', ('modification_user_ids', '=', False),
                ('id', 'in', user.modification_journal_ids.ids)]

        return super(AccountJournal, self).search(
            args, offset, limit, order, count=count)
