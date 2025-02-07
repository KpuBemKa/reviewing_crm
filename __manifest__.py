# -*- coding: utf-8 -*-
{
    "name": "reviewing_crm",
    "summary": "CRM expansion module for Reviewer project",
    "description": "CRM expansion module for Reviewer project",
    "author": "MARS",
    "category": "Reviewing/Reviewing",
    "version": "1.0",
    "application": True,
    "depends": ["base", "web", "crm"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        # ---
        "views/tasks_views.xml",
        "views/reviews_views.xml",
        "views/tags_views.xml",
        "views/menu_views.xml",
    ],
    "controllers": ["controllers.main_controller.MainController"],
    "assets": {
        "web.assets_backend": [
            "reviewing_crm/static/src/scss/style.scss",
            # ---
            "reviewing_crm/static/src/fields/audio_field/audio_field.js",
            "reviewing_crm/static/src/fields/audio_field/audio_field.xml",
            # ---
            "reviewing_crm/static/src/fields/audio_player_field/audio_player_field.js",
            "reviewing_crm/static/src/fields/audio_player_field/audio_player_field.scss",
            "reviewing_crm/static/src/fields/audio_player_field/audio_player_field.xml",
            # ---
            "reviewing_crm/static/src/fields/expandable_text_field/expandable_text_field.js",
            "reviewing_crm/static/src/fields/expandable_text_field/expandable_text_field.scss",
            "reviewing_crm/static/src/fields/expandable_text_field/expandable_text_field.xml",
            # ---
            "reviewing_crm/static/src/fields/gallery_field/gallery_field.js",
            "reviewing_crm/static/src/fields/gallery_field/gallery_field.scss",
            "reviewing_crm/static/src/fields/gallery_field/gallery_field.xml",
            # ---
            "reviewing_crm/static/src/utils/image_popup/image_popup.js",
            "reviewing_crm/static/src/utils/image_popup/image_popup.scss",
            "reviewing_crm/static/src/utils/image_popup/image_popup.xml",
        ],
    },
}
