/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { FileInput } from "@web/core/file_input/file_input"

export class ImageGalleryField extends Component {
    static template = "rvg.ImageGalleryField";
    static components = {
        FileInput,
    }
    static props = {
        ...standardFieldProps,
        acceptedFileExtensions: { type: String, optional: true },
        className: { type: String, optional: true },
        numberOfFiles: { type: Number, optional: true },
    }

    setup() {
        this.notification = useService("notification"); // For user feedback
    }

    get list() { return this.props.record.data[this.props.name] }

    get imageAttachments() {
        return this.list.records.map((record) => {
            return {
                ...record.data,
                id: record.resId,
            };
        });
    }

    getImageUrlPath(imageId) {
        return '/web/content/' + imageId
    }

    removeImage(deleteId) {
        const record = this.list.records.find(
            (record) => record.resId === deleteId
        );

        this.list.delete(record);
    }


    async onFileUploaded(files) {
        console.log("before", this.props.record.data[this.props.name]);
        for (const file of files) {
            if (file.error) {
                return this.notification.add(file.error, {
                    title: "Uploading error",
                    type: "danger",
                });
            }
        }

        this.props.record.save();
        this.props.record.load();
    }
}

export const galleryField = {
    component: ImageGalleryField,
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
    supportedTypes: ["one2many"],
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
}

registry.category("fields").add("rvg_image", galleryField);
