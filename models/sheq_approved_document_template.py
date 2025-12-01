from odoo import models, fields, api

class SheqDocumentTemplate(models.Model):
    _name = 'sheq.document.template'
    _description = 'SHEQ Document Template'
    
    name = fields.Char(string='Template Name', required=True)
    document_id = fields.Many2one('sheq.approved.document', string='Document')
    attachment = fields.Binary(string='File', required=True)
    attachment_filename = fields.Char(string='File Name')