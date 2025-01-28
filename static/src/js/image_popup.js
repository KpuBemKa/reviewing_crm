/** @odoo-module **/

import { Component, onMounted, onWillUnmount, useRef } from "@odoo/owl";

export class ImagePopup extends Component {
    setup() {
        this.state = {
            imageUrl: this.props.imageUrl,
        };

        this.popupRef = useRef("rvg_image_popup");

        this.closeOnEsc = this.closeOnEsc.bind(this);
        this.closeOnOutsideClick = this.closeOnOutsideClick.bind(this);

        onMounted(() => {
            window.addEventListener("keydown", this.closeOnEsc);

            if (this.popupRef.el) {
                this.popupRef.el.addEventListener("click", this.closeOnOutsideClick);
            }
        });

        onWillUnmount(() => {
            window.removeEventListener("keydown", this.closeOnEsc);
            if (this.popupRef.el) {
                this.popupRef.el.removeEventListener("click", this.closeOnOutsideClick);
            }
        });
    }

    closeOnEsc(event) {
        if (event.key === "Escape") {
            this.closeDialog();
        }
    }

    closeOnOutsideClick(event) {
        if (this.popupRef.el && event.target === this.popupRef.el) {
            this.closeDialog();
        }
    }

    closeDialog() {
        this.props.close();
    }
}

ImagePopup.template = "rvg.ImagePopup";
ImagePopup.props = {
    close: Function,
    imageUrl: { type: String, optional: false }, // Image URL is required
};

