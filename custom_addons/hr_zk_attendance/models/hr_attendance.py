from odoo import fields, models

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    location_id = fields.Many2one('res.partner', string='Location')
    attendance_state = fields.Selection([
        ('sign_in', 'Sign In'),
        ('sign_out', 'Sign Out')
    ], string='Attendance State')
    punch_type = fields.Selection([
        ('in', 'Check In'),
        ('out', 'Check Out')
    ], string='Punch Type') 