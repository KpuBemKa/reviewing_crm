/** @odoo-module **/

import { Component } from '@odoo/owl';
import { registry } from '@web/core/registry';
import { standardFieldProps } from '@web/views/fields/standard_field_props';
import { useService } from "@web/core/utils/hooks";
import { FileInput } from "@web/core/file_input/file_input";
import { useX2ManyCrud } from "@web/views/fields/relational_utils";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

import { ImagePopup } from "../../utils/image_popup/image_popup";

class GalleryWidget extends Component {
    static template = "rvg.ImageGalleryField";
    static components = {
        FileInput,
    };
    static props = {
        ...standardFieldProps,
        acceptedFileExtensions: { type: String, optional: true },
        className: { type: String, optional: true },
        numberOfFiles: { type: Number, optional: true },
    };

    setup() {
        this.dialogService = useService("dialog");

        this.orm = useService("orm");
        this.notification = useService("notification");
        this.operations = useX2ManyCrud(() => this.props.record.data[this.props.name], true);

        console.log(this.props);
        // console.log(this.images);
    }

    get imagesRecords() { return this.props.record.data[this.props.name] }

    get uploadText() { return "Attach images" }

    getImageUrlPath(image) {
        return image.datas_url ? image.datas_url : '/web/content/' + image.resId
    }

    openImage(image) {
        this.dialogService.add(ImagePopup, {
            imageUrl: this.getImageUrlPath(image),
        });
    }

    async onFileUploaded(files) {
        for (const file of files) {
            if (file.error) {
                return this.notification.add(file.error, {
                    title: "Uploading error",
                    type: "danger",
                });
            }
            await this.operations.saveRecord([file.id]);
        }
    }

    async onImageRemove(image_id) {
        const record = this.props.record.data[this.props.name].records.find(
            (record) => record.resId === image_id
        );

        if (typeof record === 'undefined') {
            console.error("Record not found");
            return this.notification.add(file.error, {
                title: "Deleting error",
                type: "danger",
            });
        }

        this.dialogService.add(ConfirmationDialog, {
            body: "This action will delete the image. Proceed?",
            confirmLabel: "Confirm",
            confirm: () => this.operations.removeRecord(record),
            cancelLabel: "Cancel",
            cancel: () => { }
        });
    }
}

export const galleryWidget = {
    component: GalleryWidget,
    supportedOptions: [
        {
            label: "Accepted file extensions",
            name: "accepted_file_extensions",
            type: "string",
        },
        {
            label: "Number of files",
            name: "number_of_files",
            type: "integer",
        },
    ],
    supportedTypes: ["many2many"],
    isEmpty: () => false,
    relatedFields: [
        { name: "name", type: "char" },
        { name: "mimetype", type: "char" },
    ],
    extractProps: ({ attrs, options }) => ({
        acceptedFileExtensions: options.accepted_file_extensions,
        className: attrs.class,
        numberOfFiles: options.number_of_files,
    }),
};

// export const galleryWidget = { component: GalleryWidget, };

registry.category("fields").add('rvg_gallery', galleryWidget);