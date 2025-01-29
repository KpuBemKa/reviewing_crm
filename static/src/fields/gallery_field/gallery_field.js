/** @odoo-module **/

import { Component } from '@odoo/owl';
import { registry } from '@web/core/registry';
import { standardFieldProps } from '@web/views/fields/standard_field_props';
import { useService } from "@web/core/utils/hooks";

import { ImagePopup } from "../../utils/image_popup/image_popup";

class GalleryWidget extends Component {
    setup() {
        this.dialogService = useService("dialog");

        console.log(this.props);
        // console.log(this.images);
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

    get imagesRecords() { return this.props.record.data[this.props.name] }
}

export const galleryWidget = { component: GalleryWidget, };

registry.category("fields").add('rvg_gallery', galleryWidget);

// /** @odoo-module **/

// import { Component } from '@odoo/owl';
// import { registry } from '@web/core/registry';
// import { standardFieldProps } from '@web/views/fields/standard_field_props';
// import { useService } from "@web/core/utils/hooks";
// import { ImageField } from "@web/views/fields/image/image_field.js"

// import { ImagePopup } from "./image_popup";

// class GalleryField extends ImageField {

// }

    
// export const galleryWidget = { component: GalleryField, };

// registry.category("fields").add('rvg_gallery', galleryWidget);