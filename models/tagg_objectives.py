from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class TaggObjectives(models.Model):
    _name = 'tagg.objectives'
    _description = 'TAGG Objectives'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='ID', required=True, default='New')
    
    # General Section
    objective_type = fields.Selection([
        ('strategic', 'Strategic'),
        # ('operational', 'Operational'),
        # ('departmental', 'Departmental'),
        # ('individual', 'Individual'),
    ], string='TYPE OF OBJECTIVES', required=True)
    
    subsidiary = fields.Selection([
        ('automation', 'The Automation Ghana Group Ltd: Automation'),
        ('electric', 'The Automation Ghana Group Ltd: Electric'),
        ('group', 'The Automation Ghana Group Ltd'),
    ], string='SUBSIDIARY', required=True)
    
    department = fields.Selection([
        ('sheq', 'SHEQ'),
    ], string='DEPARTMENT', default='sheq')
    revision_number = fields.Integer(string='REVISION NUMBER')
    
    status = fields.Selection([
        ('new', 'New'),
        ('draft', 'Draft'),
        ('submitted', 'Submitted for Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='STATUS', default='draft', tracking=True)
    


    compiled_by_id = fields.Many2one('res.partner', string='COMPILED BY', ondelete='set null')
    compiled_by_designation = fields.Many2one('res.users', string='COMPILED BY (DESIGNATION)', default=lambda self: self.env.user)
    
    
    rejection_reason = fields.Text(string='REJECTION REASON (CEO)')
    reference_year = fields.Integer(string='REFERENCE YEAR', default=2025)
    date = fields.Date(string='DATE', default=fields.Date.today)
    

    objective_what = fields.Text(string='WHAT WILL BE OUR ACTIONS TO BECOME WHEN MEETING')
    due_date = fields.Date(string='DUE DATE')
    how_results_measured = fields.Text(string='HOW WILL RESULTS BE MEASURED')
    which_result_emulated = fields.Text(string='WHICH RESULT WILL BE EMULATED')
    resources = fields.Text(string='RESOURCES')
    responsibility = fields.Char(string='RESPONSIBILITY')
    experimental = fields.Char(string='EXPERIMENTAL')
    pm_q1 = fields.Char(string='PM Q1')
    pm_q2 = fields.Char(string='PM Q2') 
    pm_q3 = fields.Char(string='PM Q3')
    pm_q4 = fields.Char(string='PM Q4')
    final_year = fields.Char(string='FINAL YEAR')

    @api.model
    def create(self, vals_list):
        # Ensure we don't mutate the caller's dict
        vals = dict(vals_list or {})
        # Assign a sequence name if not provided
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('tagg.objectives.sequence') or 'New'
        # If the creator didn't explicitly set a status, consider a newly
        # saved record to be in 'draft' (unless it's intentionally created
        # as 'submitted' by passing status in vals).
        if 'status' not in vals:
            vals['status'] = 'draft'
        return super().create(vals)

    def write(self, vals):
        try:
            # If the caller explicitly sets status, respect it.
            if 'status' in (vals or {}):
                return super().write(vals)

            # For records that are already submitted, do not change status.
            to_keep = self.filtered(lambda r: r.status == 'submitted')
            to_set_draft = self - to_keep

            result = True
            if to_set_draft:
                vals2 = dict(vals or {})
                vals2['status'] = 'draft'
                result = super(TaggObjectives, to_set_draft).write(vals2)
            if to_keep:
                
                result2 = super(TaggObjectives, to_keep).write(vals)
                result = result and result2
            return result
        except Exception:
            _logger.exception('Error in TaggObjectives.write with vals=%s', vals)
            raise
    
    def action_submit_approval(self):
        """Submit for approval action"""
        self.write({'status': 'submitted'})
        return True
    
    def action_approve(self):
        """Approve action"""
        self.write({'status': 'approved'})
        return True
    
    def action_reject(self):
        """Reject action"""
        self.write({'status': 'rejected'})
        return True
    
    def action_draft(self):
        """Set back to draft"""
        self.write({'status': 'draft'})
        return True
    
    def action_cancel(self):


        action = self.env.ref('tagg_academy.action_tagg_objectives')
        if action:
            return action.read()[0]
        return {'type': 'ir.actions.act_window_close'}

    def action_open_form(self):
        """Return an action that opens the form view for this record.

        This is intended to be called from a list-view button so the user
        can reliably open the form even when the row-click handler is flaky.
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }