from odoo import models, fields, api

class SheqApprovedDocument(models.Model):
    _name = 'sheq.approved.document'
    _description = 'SHEQ Approved Document'
    
    # General Section
    author = fields.Many2one('res.users', string='Author *', default=lambda self: self.env.user, required=True)
    manager_id = fields.Many2one('hr.employee', string='Manager *')
    department = fields.Selection([
        ('sheq', 'SHEQ'),
    ], string='Department *', default='sheq', required=True)
    # Details Section
    description_of_request = fields.Text(string='Description of Request')
    description_of_workflow = fields.Text(string='Description of Workflow')
    reason_not_on_odoo = fields.Text(string='State reason why Form cannot be on Odoo')

    name = fields.Char(string='Name of Record *', required=True)
    document_type = fields.Selection([
        ('procedure', 'Procedure'),
        ('work_instruction', 'Work Instruction'),
        ('form', 'Form'),
    ], string='Type of Document', required=True)
    related_oms_process = fields.Char(string='Related OMS Process')
    document_status = fields.Selection([
        ('new', 'New'),
        ('draft', 'Draft'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
    ], string='Document Status', default='new')
    date = fields.Date(string='Date', default=fields.Date.context_today)

    # For SHEQ Use Section
    is_physical_form = fields.Boolean(string='Is it a Physical Form?')
    reason_number = fields.Char(string='Reason Number')
    expected_completeion_date = fields.Date(string='Expected Completion Date')

    # Affected Departments (multi-select). Users can create new departments from the dropdown.
    affected_departments = fields.Many2many(
        'sheq.department',
        'sheq_approved_document_department_rel',
        'document_id',
        'department_id',
        string='Affected Departments',
    )
    affected_manager_1 = fields.Many2one('hr.employee', string='Affected Manager (1)')
    affected_manager_2 = fields.Many2one('hr.employee', string='Affected Manager (2)')
    affected_manager_3 = fields.Many2one('hr.employee', string='Affected Manager (3)')
    affected_manager_4 = fields.Many2one('hr.employee', string='Affected Manager (4)')
    affected_manager_5 = fields.Many2one('hr.employee', string='Affected Manager (5)')
    affected_manager_6 = fields.Many2one('hr.employee', string='Affected Manager (6)')
    affected_manager_7 = fields.Many2one('hr.employee', string='Affected Manager (7)')
    affected_manager_8 = fields.Many2one('hr.employee', string='Affected Manager (8)')
    affected_manager_9 = fields.Many2one('hr.employee', string='Affected Manager (9)')
    affected_manager_10 = fields.Many2one('hr.employee', string='Affected Manager (10)')

    # Templates
    template_attachment = fields.Binary(string='Template Attachment')
    template_filename = fields.Char(string='Template Filename')
    template_attachment_ids = fields.One2many(
        'sheq.approved.document.template',
        'document_id',
        string='Template Attachments',
    )

    # Application Specialist
    application_specialist = fields.Char(
        string='Application Specialist',
        default='The Automation Ghana Group Ltd (Provisioning - PPA SHEQ)'
    )

    # Action Methods
    def action_save(self):
        return True

    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}

    def action_submit(self):
        self.write({'document_status': 'under_review'})
        return True


class SheqDepartment(models.Model):
    _name = 'sheq.department'
    _description = 'SHEQ Department'

    name = fields.Char(string='Department', required=True)
    active = fields.Boolean(string='Active', default=True)


class SheqApprovedDocumentTemplate(models.Model):
    _name = 'sheq.approved.document.template'
    _description = 'SHEQ Approved Document Template Attachment'

    name = fields.Char(string='File Name')
    attachment = fields.Binary(string='Attachment')
    mimetype = fields.Char(string='MIME Type')
    document_id = fields.Many2one('sheq.approved.document', string='Document', ondelete='cascade')