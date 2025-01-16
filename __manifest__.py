# -*- coding: utf-8 -*-
{
    "name": "reviewing_crm",
    "summary": "CRM expansion module for Reviewer project",
    "description": "CRM expansion module for Reviewer project",
    "author": "My Company",
    "category": "Uncategorized",
    "version": "0.1",
    "depends": ["base", "web", "crm"],
    "data": [
        "views/views.xml",
        "views/templates.xml",
    ],
    "controllers": ["controllers.main_controller.MainController"],
    "assets": {
        "web.assets_backend": [
            "reviewing_crm/static/src/js/audio_field.js",
            "reviewing_crm/static/src/js/audio_player_field.js",
            "reviewing_crm/static/src/js/expandable_text_field.js",
            # ---
            "reviewing_crm/static/src/scss/audio_player_field.scss",
            "reviewing_crm/static/src/scss/expandable_text_field.scss",
            "reviewing_crm/static/src/scss/style.scss",
            # ---
            "reviewing_crm/static/src/xml/audio_field.xml",
            "reviewing_crm/static/src/xml/audio_player_field.xml",
            "reviewing_crm/static/src/xml/expandable_text_field.xml",
        ],
    },
}
