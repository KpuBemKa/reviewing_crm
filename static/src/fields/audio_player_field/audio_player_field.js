/** @odoo-module */

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

class AudioPlayerField extends Component {
    static template = "rvg.AudioPlayerTemplate";

    static props = {
        ...standardFieldProps,
    };

    get audioUrl() {
        return `/web/content/${this.props.record.model.config.resModel}/${this.props.record.resId}/${this.props.name}`;
    }
}

export const audioPlayerField = { component: AudioPlayerField, };

registry.category("fields").add("rvg_audio_player", audioPlayerField);
