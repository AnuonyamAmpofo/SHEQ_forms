from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TaggProcessRequest(models.Model):
    _name = 'tagg.process.request'
    _description = 'TAGG Process Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    # General Section
    name = fields.Char(string='Reference', required=True, default='New', copy=False)
    employee = fields.Many2one('res.users', string='Employee', 
                                           default=lambda self: self.env.user, tracking=True)
    hubat_daudi = fields.Char(string='Hubat Daudi', tracking=True)
    
    # Details Section
    type_of_request = fields.Selection([
        ('option1', 'Option 1'),
    ], string='Type of Request', required=True, tracking=True)
    tagg_process = fields.Many2one('tagg.process', string='TAGG Process', tracking=True)
    tagg_process_name = fields.Char(string='Name of TAGG Process', required=True, tracking=True)
    reason_for_request = fields.Text(string='Reason for Request', required=True, tracking=True)
    rejection_reason = fields.Text(string='Rejection Reason', tracking=True)
    
    # SHEQ Section
    requires_change_management = fields.Boolean(string='Does it require Change Management', tracking=True)
    department_id = fields.Many2one('hr.department', string='Department', required=True, tracking=True)
    subsidiary_id = fields.Many2one('res.company', string='Subsidiary', required=True, 
                                  default=lambda self: self.env.company, tracking=True)
    
    # Status
    state = fields.Selection([
        ('new', 'New'),
        ('submitted', 'Submitted for Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='new', required=True, tracking=True)
    
    # Main Fields
    
    
    # Files and Notes
    note = fields.Text(string='Notes')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments',
                                    relation='tagg_process_request_attachment_rel')
    
    # Computed fields
    display_name = fields.Char(string='Display Name', compute='_compute_display_name')
    
    @api.depends('name', 'tagg_process_name')
    def _compute_display_name(self):
        for record in self:
            if record.name and record.tagg_process_name:
                record.display_name = f"{record.name} - {record.tagg_process_name}"
            else:
                record.display_name = record.name or 'New TAGG Process Request'
    
    @api.model
    def create(self, vals_list):
        # Accept both a single vals dict (common from web client) and a list of vals
        if isinstance(vals_list, dict):
            if vals_list.get('name', 'New') == 'New':
                vals_list['name'] = self.env['ir.sequence'].next_by_code('tagg.process.request') or 'New'
            return super(TaggProcessRequest, self).create(vals_list)

        # If a list/iterable is provided, create records one-by-one so we handle
        # callers that pass multiple values while remaining compatible with the
        # web client which usually sends a single dict.
        records = self.env['tagg.process.request']
        for single_vals in vals_list:
            if isinstance(single_vals, dict) and single_vals.get('name', 'New') == 'New':
                single_vals['name'] = self.env['ir.sequence'].next_by_code('tagg.process.request') or 'New'
            rec = super(TaggProcessRequest, self).create(single_vals)
            records |= rec
        return records
    
    def action_save(self):
        """Save the form without submitting"""
        self.ensure_one()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'message': 'TAGG Process Request saved successfully.',
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
    
    def action_submit_for_approval(self):
        """Submit the request for approval"""
        self.ensure_one()
        if not self.tagg_process_name or not self.reason_for_request:
            raise ValidationError("Please fill in all required fields before submitting.")
        
        self.write({'state': 'submitted'})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'message': 'TAGG Process Request submitted for approval.',
            }
        }
    
    def action_approve(self):
        """Approve the request"""
        self.ensure_one()
        self.write({'state': 'approved'})
    
    def action_reject(self):
        """Reject the request"""
        self.ensure_one()
        if not self.rejection_reason:
            raise ValidationError("Please provide a rejection reason.")
        
        self.write({'state': 'rejected'})
    
    def action_cancel(self):
        """Cancel the request"""
        self.ensure_one()
        self.write({'state': 'new'})
    
    def action_remove_all_attachments(self):
        """Remove all attachments"""
        self.ensure_one()
        self.attachment_ids = [(5, 0, 0)]