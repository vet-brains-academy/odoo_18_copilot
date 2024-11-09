from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    zk_device_id = fields.Many2one(
        'zk.device',
        string='Biometric Device',
        tracking=True
    )
    biometric_id = fields.Char(
        string='Biometric ID',
        help='Employee ID in the biometric device',
        tracking=True
    )
    face_enrolled = fields.Boolean(
        string='Face Enrolled',
        default=False,
        tracking=True
    )
    finger_enrolled = fields.Boolean(
        string='Fingerprint Enrolled',
        default=False,
        tracking=True
    )

    _sql_constraints = [
        ('biometric_id_unique',
         'unique(biometric_id, company_id)',
         'The Biometric ID must be unique per company!')
    ]

    def action_enroll_face(self):
        """Enroll employee's face in the device"""
        self.ensure_one()
        if not self.zk_device_id:
            raise UserError(_("Please assign a biometric device first."))
        
        return {
            'name': _('Enroll Face'),
            'type': 'ir.actions.act_window',
            'res_model': 'zk.face.enroll.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_employee_id': self.id}
        } 