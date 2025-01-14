from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ReviewingLead(models.Model):
    _inherit = "crm.lead"

    rec_timestamp = fields.Datetime(string="Time of recording")
    rec_device = fields.Char(string="Recording device")
    rec_audio_file = fields.Binary(string="Audio file")
    rec_filename = fields.Char(string="Audio file name")
    rec_transcription = fields.Text(string="Text review")

    @api.constrains("rec_audio_file")
    def _check_date_end(self):
        for record in self:
            if not record.rec_filename.endswith((".wav", ".ogg", ".mp3")):
                raise ValidationError("Uploaded file should be a .wav file.")
