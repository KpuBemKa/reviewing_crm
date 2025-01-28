# -*- coding: utf-8 -*-
{
    "name": "reviewing_crm",
    "summary": "CRM expansion module for Reviewer project",
    "description": "CRM expansion module for Reviewer project",
    "author": "My Company",
    "category": "Reviewing/Reviewing",
    "version": "0.1",
    "depends": ["base", "web"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        # ---
        "views/templates.xml",
        "views/tasks_views.xml",
        "views/reviews_views.xml",
        "views/menu_views.xml",
    ],
    "controllers": ["controllers.main_controller.MainController"],
    "assets": {
        "web.assets_backend": [
            "reviewing_crm/static/src/js/audio_field.js",
            "reviewing_crm/static/src/js/audio_player_field.js",
            "reviewing_crm/static/src/js/expandable_text_field.js",
            "reviewing_crm/static/src/js/gallery_field.js",
            "reviewing_crm/static/src/js/image_popup.js",
            # ---
            "reviewing_crm/static/src/scss/audio_player_field.scss",
            "reviewing_crm/static/src/scss/expandable_text_field.scss",
            "reviewing_crm/static/src/scss/gallery_field.scss",
            "reviewing_crm/static/src/scss/image_popup.scss",
            "reviewing_crm/static/src/scss/style.scss",
            # ---
            "reviewing_crm/static/src/xml/audio_field.xml",
            "reviewing_crm/static/src/xml/audio_player_field.xml",
            "reviewing_crm/static/src/xml/expandable_text_field.xml",
            "reviewing_crm/static/src/xml/gallery_field.xml",
            "reviewing_crm/static/src/xml/image_popup.xml",
        ],
    },
}
