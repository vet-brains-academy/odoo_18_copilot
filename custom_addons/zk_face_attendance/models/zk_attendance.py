from odoo import models, fields, api, _
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class ZKAttendance(models.Model):
    _name = 'zk.attendance'
    _description = 'ZK Device Attendance'
    _order = 'timestamp DESC'

    employee_id = fields.Many2one(
        'hr.employee', 
        string='Employee',
        required=True,
        index=True
    )
    device_id = fields.Many2one(
        'zk.device',
        string='Device',
        required=True,
        index=True
    )
    timestamp = fields.Datetime(
        string='Timestamp',
        required=True,
        index=True
    )
    attendance_type = fields.Selection([
        ('check_in', 'Check In'),
        ('check_out', 'Check Out')
    ], string='Type', required=True)
    
    punch_type = fields.Selection([
        ('face', 'Face'),
        ('finger', 'Fingerprint'),
        ('password', 'Password'),
        ('card', 'Card')
    ], string='Punch Type')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validated', 'Validated'),
        ('error', 'Error')
    ], string='Status', default='draft')
    
    attendance_id = fields.Many2one(
        'hr.attendance',
        string='HR Attendance',
        readonly=True
    )

    _sql_constraints = [
        ('unique_attendance',
         'unique(employee_id, device_id, timestamp)',
         'Attendance record already exists!')
    ]

    def action_validate(self):
        """Validate attendance and create hr.attendance record"""
        for record in self:
            if record.state != 'draft':
                continue

            try:
                # Find existing attendance record
                attendance = self.env['hr.attendance'].search([
                    ('employee_id', '=', record.employee_id.id),
                    ('check_in', '<=', record.timestamp),
                    ('check_out', '=', False)
                ], limit=1)

                if record.attendance_type == 'check_in':
                    if attendance:
                        # Close existing attendance
                        attendance.check_out = record.timestamp
                    # Create new attendance
                    attendance = self.env['hr.attendance'].create({
                        'employee_id': record.employee_id.id,
                        'check_in': record.timestamp,
                    })
                elif record.attendance_type == 'check_out' and attendance:
                    attendance.check_out = record.timestamp

                record.write({
                    'state': 'validated',
                    'attendance_id': attendance.id if attendance else False
                })

            except Exception as e:
                _logger.error(f"Error validating attendance: {e}")
                record.write({'state': 'error'})

    @api.model
    def process_attendance(self, employee_id, timestamp, device_id, punch_type='face'):
        """Process attendance data from device"""
        # Determine check in/out based on last attendance
        last_attendance = self.search([
            ('employee_id', '=', employee_id),
            ('timestamp', '<', timestamp)
        ], limit=1, order='timestamp DESC')

        attendance_type = 'check_out' if last_attendance and \
                         last_attendance.attendance_type == 'check_in' else 'check_in'

        # Create attendance record
        attendance = self.create({
            'employee_id': employee_id,
            'device_id': device_id,
            'timestamp': timestamp,
            'attendance_type': attendance_type,
            'punch_type': punch_type
        })

        # Validate immediately
        attendance.action_validate()
        return attendance 