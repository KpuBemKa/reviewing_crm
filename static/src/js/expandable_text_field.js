/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { TextField } from "@web/views/fields/text/text_field";
import { registry } from "@web/core/registry";
import { useState, useRef, onMounted, onWillUnmount } from "@odoo/owl";

export class ExpandableTextField extends TextField {
    setup() {
        super.setup();

        this.state = useState({
            isExpanded: false,
            isOverflowing: false,
        });

        this.textContainerRef = useRef("textContainer");
        this.resizeObserver = null;

        onMounted(() => {
            this.initializeResizeObserver();
        });

        onWillUnmount(() => {
            if (this.resizeObserver) {
                this.resizeObserver.disconnect();
            }
        });
    }

    initializeResizeObserver() {
        const textContainer = this.textContainerRef.el;

        if (!textContainer) return;

        const checkOverflow = () => {
            if (!textContainer.offsetParent)
                return;

            const isOverflowing =
                textContainer.scrollWidth > textContainer.clientWidth ||
                textContainer.scrollHeight > textContainer.clientHeight;

            if (isOverflowing !== this.state.isOverflowing) {
                this.state.isOverflowing = isOverflowing;
            }
        };

        checkOverflow();

        this.resizeObserver = new ResizeObserver(() => checkOverflow());
        this.resizeObserver.observe(textContainer);
    }

    toggleExpand() {
        this.state.isExpanded = !this.state.isExpanded;
    }

    get displayText() {
        return this.props.record.data[this.props.name] || "";
    }

    get canExpand() {
        return this.state.isExpanded || this.state.isOverflowing;
    }
}

ExpandableTextField.template = "rvg.ExpandableTextFieldTemplate";

export const expandableTextField = {
    component: ExpandableTextField,
    displayName: _t("Expandable Multiline Text"),
};

registry.category("fields").add("rvg_expandable_text", expandableTextField);
