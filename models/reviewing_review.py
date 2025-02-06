from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ReviewingReview(models.Model):
    _name = "rvg.reviews"
    _description = "Reviews"
    _order = "rvg_timestamp"

    rvg_timestamp = fields.Datetime(string="Time of recording")
    rvg_device = fields.Char(string="Recording device")
    rvg_audio_file = fields.Binary(string="Audio file")
    rvg_filename = fields.Char(string="Audio file name")

    rvg_transcription = fields.Text(string="Text review")
    rvg_summary = fields.Text(string="Summary")
    rvg_issues = fields.Text(string="Issues")

    @api.constrains("rvg_audio_file")
    def _check_file_extension(self):
        for record in self:
            if record.rvg_filename and not record.rvg_filename.endswith(
                (".wav", ".ogg", ".mp3", ".mp4a")
            ):
                raise ValidationError(
                    "Uploaded file should be an audio file: wav, mp3, ogg."
                    f"Filename: '{record.rvg_filename}'."
                )
