import base64
import logging
import traceback
import ast

from datetime import datetime, timezone, timedelta
from odoo import http, fields, SUPERUSER_ID
from odoo.http import request, Response

from ..models.reviewing_review import ReviewingReview
from ..models.reviewing_task import ReviewingTask

from .keys import UPLAOD_API_KEY


_logger = logging.getLogger(__name__)


class UploadRecController(http.Controller):
    @http.route("/rvg/new_rec", type="http", auth="none", methods=["POST"], csrf=False)
    def add_recording(self, **kwargs):
        api_key = request.httprequest.headers.get("API-Key")
        if not api_key or not self._validate_api_key(api_key):
            _logger.warning(
                f"Unauthorized request from '{request.httprequest.remote_addr}'"
            )
            return Response("Unauthorized", status=401)

        try:
            uploaded_file = request.httprequest.files.get("file")
            if not uploaded_file:
                _logger.warning(
                    f"No file provided in the request from '{request.httprequest.remote_addr}'"
                )
                return Response("No file provided", status=400)

            file_name: str = str(kwargs.get("file_name"))
            issues_list: list[dict[str, str]] = ast.literal_eval(
                str(kwargs.get("issues"))
            )

            new_review = self._create_review(
                timestamp=file_name[file_name.find("_") + 1 : file_name.rfind(".")],
                file_content=uploaded_file.read(),
                file_name=file_name,
                transcription=str(kwargs.get("transcription")),
                summary=str(kwargs.get("summary")),
                issues=issues_list,
            )

            new_task = self._create_task(new_review, issues_list)

            _logger.info(
                f"New review has been uploaded from '{request.httprequest.remote_addr}'"
                f"and saved as record #{new_review.id} with file name '{file_name}'"
            )

            return Response(
                f"Review added successfully with ID {new_review.id}", status=200
            )
        except Exception as e:
            _logger.error(
                f"Exception occured during request handling from '{request.httprequest.remote_addr}'"
                f".\nTraceback:\n{traceback.format_exc()}"
            )
            return Response(f"Error: {e}", status=500)

    def _validate_api_key(self, api_key: str) -> bool:
        return api_key == UPLAOD_API_KEY

    def _create_review(
        self,
        timestamp: str,
        file_content: bytes,
        file_name: str,
        transcription: str,
        summary: str,
        issues: list[dict[str, str]],
    ) -> ReviewingReview:
        return (
            request.env["rvg.reviews"]
            .with_user(SUPERUSER_ID)
            .create(
                {
                    "rvg_timestamp": fields.Datetime.from_string(
                        datetime.fromtimestamp(
                            int(timestamp), tz=timezone.utc
                        ).strftime("%Y-%m-%d %H:%M:%S")
                    ),
                    "rvg_device": file_name[: file_name.find("_")],
                    "rvg_audio_file": base64.b64encode(file_content).decode("utf-8"),
                    "rvg_filename": file_name,
                    "rvg_transcription": transcription,
                    "rvg_summary": summary,
                    "rvg_issues": "\n".join(issue["description"] for issue in issues),
                }
            )
        )

    def _create_task(
        self, review: ReviewingReview, issues: list[dict[str, str]]
    ) -> ReviewingTask:
        device_tag = self._get_device_tag_id(review.rvg_device)
        issues_tags = self._get_tags_with_names(
            [issue["departments"] for issue in issues]
        )
        responsible_user_id = self._get_user_by_login("no-email@joe.com.tv")

        new_task = (
            request.env["rvg.tasks"]
            .with_user(SUPERUSER_ID)
            .create(
                {
                    "rvg_title": review.rvg_device,
                    "rvg_expected_closing": fields.Datetime.now(),
                    "rvg_responsible": responsible_user_id,
                    "rvg_tag_ids": issues_tags + device_tag,
                    "rvg_review_id": review.id,
                }
            )
        )

        new_task.activity_schedule(
            act_type_xmlid="mail.mail_activity_data_todo",
            date_deadline=fields.Datetime.today() + timedelta(days=5),
            summary="It should be a summary in here.",
            note="It should be a note here.",
            user_id=responsible_user_id,
        )
        
        return new_task

    def _get_tags_with_names(self, tag_names: list[str]) -> list[int]:
        domain: list[str | tuple] = ["|"] * (len(tag_names) - 1)
        for tag in tag_names:
            domain.append(("name", "=ilike", tag))

        records = request.env["rvg.tags"].with_user(SUPERUSER_ID).search(domain)

        return [record["id"] for record in records]

    def _get_device_tag_id(self, device_name: str) -> list[int]:
        return self._get_tags_with_names([self._get_device_tag_name((device_name))])

    def _get_device_tag_name(self, device_name: str) -> str:
        if "tg" in device_name:
            return "Telegram"

        if "wtsp" in device_name:
            return "Whatsapp"

        if "esp" in device_name:
            return "Microphone"

        return ""

    def _get_user_by_login(self, login: str) -> int:
        return (
            request.env["res.users"]
            .with_user(SUPERUSER_ID)
            .search([("login", "=", login)], limit=1)
            .id
        )
