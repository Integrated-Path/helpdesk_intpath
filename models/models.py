# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class HelpDeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    ticket_type_id = fields.Many2one('helpdesk.ticket.type', string='Ticket Type', required=True)
    steps_to_follow = fields.Text(string='Steps to follow',required=True)
 
    expected_behavior = fields.Char('Expected Behavior' , required=True)
    current_behavior = fields.Char(string='Current Behavior',required=True)
    users_names = fields.Char(string='Users Names', required=True)
    related_record_name = fields.Char(string='Related Record Name', required=True)
    Attachments = fields.Char(string='Attachments', required=True)
    error_message = fields.Char(string='Error Message') 
    other_info = fields.Char(string='Other Info')
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
