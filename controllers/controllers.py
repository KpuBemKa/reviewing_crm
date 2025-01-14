import base64
import logging
from datetime import datetime, timezone
from odoo import http, fields
from odoo.http import request, Response

from .keys import UPLAOD_API_KEY


_logger = logging.getLogger(__name__)


class MainController(http.Controller):
    @http.route("/recs/new_rec", type="http", auth="none", methods=["POST"], csrf=False)
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

            # Save the file to the database
            file_name: str = kwargs.get("file_name")
            file_content = uploaded_file.read()
            transcription = kwargs.get("transcription")
            timestamp: str = file_name[file_name.find("_") + 1 : file_name.rfind(".")]
            # print(f"Timestamp: {timestamp}")

            new_record = (
                request.env["recs.recordings"]
                .sudo()
                .create(
                    {
                        "rec_timestamp": fields.Datetime.from_string(
                            datetime.fromtimestamp(
                                int(timestamp), tz=timezone.utc
                            ).strftime("%Y-%m-%d %H:%M:%S")
                        ),
                        "rec_device": file_name[: file_name.find("_")],
                        "rec_audio_file": base64.b64encode(file_content).decode(
                            "utf-8"
                        ),
                        "rec_filename": file_name,
                        "rec_transcription": transcription,
                    }
                )
            )

            _logger.info(
                f"New file has been uploaded from '{request.httprequest.remote_addr}'"
                f"and saved as record #{new_record.id} with file name '{file_name}'"
            )

            return Response(
                f"File uploaded successfully with ID {new_record.id}", status=200
            )
        except Exception as e:
            _logger.error(
                f"Exception occured during request handling from '{request.httprequest.remote_addr}'.\nTraceback:\n{e}"
            )
            return Response(f"Error saving file: {e}", status=500)

    def _validate_api_key(self, api_key: str) -> bool:
        return api_key == UPLAOD_API_KEY
