// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { ILabShell, ILayoutRestorer } from '@jupyterlab/application';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import { DocumentOfContent } from './doc';
import { requestAPI } from './api';
import '../style/index.css';
/**
 * Activates the ToC extension.
 *
 * @private
 * @param app - Jupyter application
 * @param docmanager - document manager
 * @param editorTracker - editor tracker
 * @param labShell - Jupyter lab shell
 * @param restorer - application layout restorer
 * @param markdownViewerTracker - Markdown viewer tracker
 * @param notebookTracker - notebook tracker
 * @param rendermime - rendered MIME registry
 * @returns table of contents registry
 */
function activateDOC(app, docmanager, labShell, restorer, rendermime) {
    const getCodelabURL = async function () {
        const res = await requestAPI('getCodeLabDocument', {
            method: 'GET'
        });
        if (res.status == 200) {
            var url = res.data;
            var tab = new DocumentOfContent({
                docmanager,
                rendermime,
                url
            });
            tab.title.iconClass = 'jp-BookOfContents-icon jp-SideBar-tabIcon';
            tab.title.caption = '操作手册';
            tab.id = 'table-of-contents';
            labShell.add(tab, 'right', {
                activate: true,
                rank: 0
            });
            restorer.add(tab, 'codeLab-handbook');
        }
    };
    getCodelabURL();
}
/**
 * Initialization data for the ToC extension.
 *
 * @private
 */
const extension = {
    id: '@blackwalnutlab/gitbook',
    autoStart: true,
    requires: [
        IDocumentManager,
        ILabShell,
        ILayoutRestorer,
        IRenderMimeRegistry,
    ],
    activate: activateDOC
};
/**
 * Exports.
 */
export default extension;
