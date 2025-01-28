from odoo import models, fields
# from odoo import models, fields, api
# from odoo.exceptions import ValidationError


class ReviewingTask(models.Model):
    _name = "rvg.tasks"
    _description = "Tasks"

    # ---
    # Default fields
    state = fields.Selection(
        selection=[
            ("complaint", "Complaint"),
            ("in_progress", "In progress"),
            ("under_review", "Under review"),
            ("resolved", "Resolved"),
        ],
        string="State",
        default="complaint",
        required=True,
    )

    # ---
    # Main fields
    rvg_title = fields.Char(string="Title")
    rvg_review = fields.Many2one("rvg.reviews", string="Review")

    # ---
    # Main page fields
    rvg_expected_closing = fields.Date(string="Expected closing")
    rvg_responsible = fields.Many2one("res.users", string="Responsible")
    rvg_priority = fields.Selection(
        selection=[
            ("0", "Low"),
            ("1", "Medium"),
            ("2", "High"),
            ("3", "Very High"),
        ],
        string="Priority",
        default="1",
        required=True,
    )
    rvg_tag_ids = fields.Many2many(
        "rvg.tags",
        "rvg_tag_rel",
        "task_id",
        "tag_id",
        string="Tags",
        help="Classify and analyze your lead/opportunity categories like: Training, Service",
    )

    # ---
    # Review Details page
    rvg_review_timestamp = fields.Datetime(
        string="Time of recording", related="rvg_review.rvg_timestamp"
    )
    rvg_review_audio_file = fields.Binary(
        string="Audio file", related="rvg_review.rvg_audio_file"
    )
    rvg_review_filename = fields.Char(
        string="File name", related="rvg_review.rvg_filename"
    )
    rvg_review_transcription = fields.Text(
        string="Text review", related="rvg_review.rvg_transcription"
    )
    rvg_review_issues = fields.Text(string="Issues", related="rvg_review.rvg_issues")
    rvg_review_summary = fields.Text(string="Summary", related="rvg_review.rvg_summary")

    # ---
    # Resolution page
    rvg_resoltution_photos = fields.One2many(
        "ir.attachment",
        "res_id",
        domain=[("res_model", "=", "rvg.tasks")],
        string="Images",
    )
    # rvg_resoltution_photos = fields.Many2many(
    #     "ir.attachment",
    #     string="Images",
    #     domain=[("mimetype", "ilike", "image")],  # Ensures only images are shown
    #     help="Upload multiple images for the gallery",
    # )
    # rvg_resolution_details = fields.Text()
    # rvg_resoltution_photos = fields.Image(string="Image", max_width=256, max_height=256)
    # rvg_resoltution_photos_ids = fields.One2many(
    #     "rvg.tasks.images", "model_id", string="Images"
    # )
    rvg_resolution_details = fields.Text()

    # def action_open_gallery(self):
    #     self.ensure_one()
    #     return {
    #         "type": "ir.actions.act_url",
    #         "url": f"/reviewing_crm/{self.id}/gallery",
    #         "target": "self",
    #     }
