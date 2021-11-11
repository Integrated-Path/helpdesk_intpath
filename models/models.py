# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class HelpDeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'


    @api.model
    def create(self,vals):
        res = super(HelpDeskTicket,self).create(vals)
        channel = self.env['mail.channel'].search([('name', '=', res.team_id.name)], limit=1)

        if not channel:
            channel = res.env['mail.channel'].create({
            'name': res.team_id.name,
            })
        res.message_post(
            body= 'the following ticket was created.',
            message_type='notification',
            subtype_id = self.env.ref('mail.mt_comment').id,
            channel_ids= [channel.id],
            partner_ids= [partner_id.id for partner_id in channel.channel_partner_ids]
            )
                     
        return res
