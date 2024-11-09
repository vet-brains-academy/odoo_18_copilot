from struct import pack, unpack
from .zkconst import *
import socket
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ZKDevice(models.Model):
    _name = 'zk.device'
    _description = 'ZKTeco Device'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Device Name', 
        required=True,
        tracking=True
    )
    ip_address = fields.Char(
        string='IP Address', 
        required=True,
        tracking=True
    )
    port = fields.Integer(
        string='Port', 
        default=DEF_PORT,  # Using constant from zkconst
        tracking=True
    )
    timeout = fields.Integer(
        string='Timeout',
        default=DEF_TIMEOUT,  # Using constant from zkconst
        tracking=True
    )
    password = fields.Char(
        string='Password',
        help='Device communication password if any'
    )
    force_udp = fields.Boolean(
        string='Force UDP',
        help='Force UDP communication instead of TCP',
        default=False
    )
    device_state = fields.Selection([
        (str(DISABLED), 'Disabled'),  # Using constants from zkconst
        (str(ENABLED), 'Enabled')
    ], string='Device State', default=str(ENABLED))

    def create_socket(self):
        """Create socket connection to the device"""
        try:
            if self.force_udp:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.ip_address, self.port))
            return True
        except Exception as e:
            _logger.error(f"Socket creation failed: {str(e)}")
            return False

    def create_header(self, command, command_string, session_id, reply_id):
        """Create data packet header"""
        buf = pack('HHHH', command, 0, session_id, reply_id)
        buf = buf + command_string.encode() + SHORT_ZERO
        buf = pack('H', len(buf)) + buf
        buf = START_TAG.to_bytes(1, 'big') + START_TAG2.to_bytes(1, 'big') + buf
        return buf

    def send_command(self, command, command_string='', session_id=0, reply_id=0):
        """Send command to the device"""
        try:
            buf = self.create_header(command, command_string, session_id, reply_id)
            self.socket.send(buf)
            
            try:
                response = self.recv_long()
                command = unpack('HHHH', response[:8])[0]
                if command == CMD_ACK_OK:
                    return True
                elif command == CMD_ACK_ERROR:
                    return False
                elif command == CMD_ACK_DATA:
                    return response[8:]
            except Exception as e:
                _logger.error(f"Error receiving response: {str(e)}")
                return False
                
        except Exception as e:
            _logger.error(f"Error sending command: {str(e)}")
            return False

    def connect(self):
        """Connect to the device"""
        self.ensure_one()
        try:
            if not self.create_socket():
                raise UserError(_("Could not create socket connection"))

            self.send_command(CMD_CONNECT)
            return True
        except Exception as e:
            raise UserError(_(f"Connection failed: {str(e)}"))

    def disconnect(self):
        """Disconnect from the device"""
        self.ensure_one()
        try:
            self.send_command(CMD_EXIT)
            self.socket.close()
            return True
        except Exception as e:
            _logger.error(f"Error disconnecting: {str(e)}")
            return False

    def enable_device(self):
        """Enable the device"""
        return self.send_command(CMD_ENABLEDEVICE)

    def disable_device(self):
        """Disable the device"""
        return self.send_command(CMD_DISABLEDEVICE)

    def get_attendance_log(self):
        """Get attendance records from the device"""
        try:
            self.send_command(CMD_PREPARE_DATA, '1')  # Request attendance data
            response = self.send_command(CMD_DATA)
            if response:
                # Process attendance data here
                return response
            return False
        except Exception as e:
            _logger.error(f"Error getting attendance log: {str(e)}")
            return False