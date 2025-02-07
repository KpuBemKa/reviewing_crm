from odoo import models, fields, api


REVIEW_STAGES = [
    ("complaint", "Complaint"),
    ("in_progress", "In progress"),
    ("under_review", "Under review"),
    ("resolved", "Resolved"),
]


class ReviewingTask(models.Model):
    _name = "rvg.tasks"
    _description = "Tasks"
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
    ]

    # ---
    # Default fields
    rvg_stage = fields.Selection(
        selection=REVIEW_STAGES,
        group_expand="_get_review_stages",
        string="Stage",
        default="complaint",
        required=True,
    )

    # ---
    # Main fields
    rvg_title = fields.Char(string="Title")
    rvg_color = fields.Integer("Color Index", default=0)

    # ---
    # Main page fields
    rvg_expected_closing = fields.Date(string="Expected closing")
    rvg_responsible = fields.Many2one(comodel_name="res.users", string="Responsible")
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
        comodel_name="rvg.tags",
        relation="rvg_tag_rel",
        column1="task_id",
        column2="tag_id",
        string="Tags",
        help="Classify and analyze your lead/opportunity categories like: Training, Service",
    )

    # ---
    # Review Details page
    rvg_review_id = fields.Many2one(comodel_name="rvg.reviews", string="Review")
    rvg_review_timestamp = fields.Datetime(
        string="Time of recording", related="rvg_review_id.rvg_timestamp"
    )
    rvg_review_audio_file = fields.Binary(
        string="Audio file", related="rvg_review_id.rvg_audio_file"
    )
    rvg_review_filename = fields.Char(
        string="File name", related="rvg_review_id.rvg_filename"
    )
    rvg_review_transcription = fields.Text(
        string="Text review", related="rvg_review_id.rvg_transcription"
    )
    rvg_review_issues = fields.Text(string="Issues", related="rvg_review_id.rvg_issues")
    rvg_review_summary = fields.Text(string="Summary", related="rvg_review_id.rvg_summary")

    # ---
    # Resolution tab
    rvg_resoltution_photos = fields.One2many(
        comodel_name="ir.attachment",
        inverse_name="res_id",
        domain=[("res_model", "=", "rvg.tasks")],
        string="Images",
    )
    rvg_resolution_details = fields.Text(string="Resolution details")

    @api.model
    def _get_review_stages(self, values, domain, order):
        return ["complaint", "in_progress", "under_review", "resolved"]
