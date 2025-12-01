from odoo import models, fields, api

class IncidentRegister(models.Model):
    _name = 'incident.register'
    _description = 'TAGG Incident Register'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='INCIDENT REPORT NO.', required=True, default=lambda self: self._get_default_name(), copy=False)
    incident_classification = fields.Selection(selection=[('critical', 'Critical')], string='INCIDENT REPORT CLASSIFICATION', required=True, tracking=True)
    reported_by = fields.Char(string='REPORTED BY', required=True, tracking=True, placeholder="Type then tab")
    

    investigation_department = fields.Char(string='DEPARTMENT RESPONSIBLE FOR INCIDENT INVESTIGATION', tracking=True, required=True)
    investigation_status = fields.Selection(selection=[("open", "Open")], string='INCIDENT INVESTIGATION REPORT STATUS', tracking=True, required=True, default='open')
    

    employee_discussion_status = fields.Selection(selection=[("open", "Open")], string='STATUS OF DISCUSSION WITH EMPLOYEES', tracking=True, placeholder="Type then tab", required=True, default='open')
    description = fields.Text(string='BRIEF DESCRIPTION OF THE INCIDENT', required=True)
    
    incident_date = fields.Date(string='DATE OF THE INCIDENT', default=fields.Date.today, required=True)
    submission_date = fields.Date(string='SUBMISSION DATE FOR INCIDENT INVESTIGATION REPORT', required=True)
    further_investigation_status = fields.Selection(selection=[], string='STATUS OF FURTHER INVESTIGATION REPORTS (IF NEEDED)', tracking=True)
    
    
    date_reported = fields.Date(string='DATE REPORTED TO HSE', default=fields.Date.today, tracking=True)
    time_of_incident = fields.Float(string='TIME OF INCIDENT', required=True, tracking=True)
    location = fields.Char(string='LOCATION OF INCIDENT', required=True, tracking=True)
    injuries_count = fields.Integer(string='NUMBER OF INJURIES / ILLNESSES RECORDED', default=0, required=True)
    
    action_lists_generated = fields.Text(string='ACTION LISTS GENERATED', tracking=True)
    closure_status = fields.Selection(selection=[('open', 'Open')], string='CLOSURE STATUS', tracking=True, default='open')
    effectiveness_assessment = fields.Text(string='ASSESS EFFECTIVENESS OF ALL ACTIONS IMPLEMENTED', required=True, tracking=True, placeholder="Describe the effectiveness of corrective actions...")

    @api.model
    def _get_default_name(self):
        sequence = self.env['ir.sequence'].next_by_code('incident.register.sequence') or 'NEW'
        return sequence

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', 'NEW') == 'NEW':
            vals_list['name'] = self._get_default_name()
        return super(IncidentRegister, self).create(vals_list)
    
    def action_save(self):


        if not self.description:
            raise ValueError("A brief description is required before you can save this report.")
        return True

    # @api.model
    def action_cancel_form(self):
        """Go back to the list view without saving."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Incident Register',
            'res_model': 'incident.register',
            'view_mode': 'list,form',
            'target': 'current',
        }