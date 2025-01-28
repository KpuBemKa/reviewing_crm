/** @odoo-module **/

import { Component } from '@odoo/owl';
import { registry } from '@web/core/registry';
import { standardFieldProps } from '@web/views/fields/standard_field_props';
import { useService } from "@web/core/utils/hooks";

import { ImagePopup } from "./image_popup";

class GalleryWidget extends Component {
    setup() {
        this.dialogService = useService("dialog");

        console.log(this.props)
    }

    static template = "rvg.GalleryWidget";

    static props = {
        ...standardFieldProps,
        record: Object,
    };

    getImageUrlPath(image) {
        return image.datas_url ? image.datas_url : '/web/content/' + image.resId
    }

    openImage(image) {
        // this.dialogService.add(ImageDialog, { imageUrl: this.getImageUrlPath(image) })

        this.dialogService.add(ImagePopup, {
            imageUrl: this.getImageUrlPath(image),
        });
    }
}

export const galleryWidget = { component: GalleryWidget, };

registry.category("fields").add('rvg_gallery', galleryWidget);
