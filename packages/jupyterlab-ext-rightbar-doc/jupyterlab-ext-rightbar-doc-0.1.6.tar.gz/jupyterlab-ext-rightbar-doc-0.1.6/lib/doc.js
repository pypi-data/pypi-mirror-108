// Copyright (c) 福建星网视易信息系统有限公司
// Distributed under the terms of the Modified BSD License.
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { Widget } from '@lumino/widgets';
/**
 * Widget for hosting a notebook document of contents.
 */
export class DocumentOfContent extends Widget {
    /**
     * Returns a new table of contents.
     *
     * @param options - options
     * @returns widget
     */
    constructor(options) {
        super();
        this._url = options.url;
    }
    /**
     * Callback invoked upon an update request.
     *
     * @param msg - message
     */
    onUpdateRequest(msg) {
        this.updateDOC();
    }
    updateDOC() {
        let title = '操作手册';
        let url = this._url;
        let renderedJSX = (React.createElement("div", { className: "jp-BookOfContents" }, React.createElement("header", null, title), React.createElement("iframe", { style: {
                width: '100%',
                height: '100%'
            }, src: url })));
        ReactDOM.render(renderedJSX, this.node, () => { });
    }
    /**
     * Callback invoked to re-render after showing a table of contents.
     *
     * @param msg - message
     */
    onAfterShow(msg) {
        this.update();
    }
}
