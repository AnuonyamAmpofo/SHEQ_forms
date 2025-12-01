from odoo import models, fields, api

class TaggProcess(models.Model):
    _name = 'tagg.process'
    _description = 'TAGG Process'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    # Main fields
    name = fields.Char(string='Name', required=True, default='New')
    process_category = fields.Selection([
        ('operational', 'Operational'),
        ('management', 'Management'),
        ('support', 'Support'),
    ], string='Process Category', required=True)
    related_change_management = fields.Char(string='Related Change Management')
    subsidiary_id = fields.Many2one('res.company', string='Subsidiary', required=True)
    department_id = fields.Many2one('hr.department', string='Department', required=True)
    
    # Process flow
    input_source = fields.Char(string='Input Source', required=True)
    process_input = fields.Char(string='Process Input', required=True)
    process_outputs = fields.Char(string='Process Outputs', required=True)
    recipients_of_outputs = fields.Char(string='Recipients of Outputs', required=True)  # Added missing field
    specifications_of_outputs = fields.Text(string='Specifications of Outputs')
    
    # Process details
    persons_responsible = fields.Char(string='Persons Responsible', required=True)  # Added required=True
    process_objectives = fields.Text(string='Process Objectives', required=True)  # Added required=True
    resources_required = fields.Text(string='Resources Required', required=True)  # Added required=True
    
    # Associated documents
    associated_sops = fields.Char(string='Associated SOP(s)')
    associated_guidelines = fields.Char(string='Associated Guidelines')
    associated_policies = fields.Char(string='Associated Policies')
    process_diagram = fields.Char(string='Process Diagram')

    # Files field changed from Binary to Many2many for multiple file support
    files = fields.Many2many('ir.attachment', string='Files')
    notes = fields.Text(string='Notes')
    
    # State and status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted to SHEQ'),
        ('approved', 'Approved'),
        ('void', 'Void')
    ], string='Status', default='draft', tracking=True)
    
    # Alias for state to match view field name
    status = fields.Selection(related='state', string='Status', readonly=True)
    
    # One2many fields for the tabs
    qms_risk_ids = fields.One2many('tagg.process.qms.risk', 'process_id', string='QMS Risks')
    hse_risk_ids = fields.One2many('tagg.process.hse.risk', 'process_id', string='HSE Risks')
    opportunity_ids = fields.One2many('tagg.process.opportunity', 'process_id', string='Opportunities')
    legal_requirement_ids = fields.One2many('tagg.process.legal.requirement', 'process_id', string='Legal Requirements')
    
    # Methods
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.name == 'New':
                # Auto-generate sequence
                last_record = self.search([('name', '!=', 'New')], order='id desc', limit=1)
                if last_record and last_record.name.isdigit():
                    next_number = int(last_record.name) + 1
                else:
                    next_number = 1
                record.name = str(next_number)
        return records
    
    def action_submit_sheq(self):
        self.write({'state': 'submitted'})
    
    def action_approve(self):
        self.write({'state': 'approved'})
    
    def action_void(self):
        self.write({'state': 'void'})
    
    def action_draft(self):
        self.write({'state': 'draft'})

    def action_save(self):
        """Save action called from the form header.

        The web client normally handles saving automatically. This server
        method is a lightweight stub so views that call `type="object"`
        for Save don't fail with a missing-method error. It returns True
        to indicate success.
        """
        # No extra server-side work required here; returning True is enough
        # for the button to behave like a no-op server action.
        return True

    def action_cancel(self):
        """Cancel action invoked from the form header.

        Return the module's list action so the client navigates back to the
        TAGG Processes list. Falls back to closing the action if the action
        xmlid cannot be found.
        """
        action = self.env.ref('tagg_academy.action_tagg_process', raise_if_not_found=False)
        if action:
            return action.read()[0]
        return {'type': 'ir.actions.act_window_close'}