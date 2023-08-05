(self["webpackChunkjupyterlab_fileopen"] = self["webpackChunkjupyterlab_fileopen"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab-fileopen', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DummyWidget": () => (/* binding */ DummyWidget),
/* harmony export */   "FileOpenFactory": () => (/* binding */ FileOpenFactory),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");








const selectorItem = '.jp-DirListing-item[data-isdir]';
const selectorNotDir = '.jp-DirListing-item[data-isdir="false"]';
const SETTINGS_ID = 'jupyterlab-fileopen:jupyterlab-fileopen-settings';
/**
 * The command IDs.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.openFileExplorer = 'jupyterlab-fileopen:open-file-explorer';
    CommandIDs.openFile = 'jupyterlab-fileopen:open-file';
})(CommandIDs || (CommandIDs = {}));
/**
 * A widget that does not will to live.
 */
class DummyWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    onAfterAttach() {
        var _a;
        (_a = this.parent) === null || _a === void 0 ? void 0 : _a.dispose();
    }
}
/**
 * A widget factory for opening files with the default desktop application.
 */
class FileOpenFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_3__.ABCWidgetFactory {
    /**
     * Create a new widget factory.
     */
    constructor(options, app) {
        super(options);
        this.app = app;
    }
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        this.app.commands.execute(CommandIDs.openFile);
        return new _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_3__.DocumentWidget({
            context,
            content: new DummyWidget()
        });
    }
}
/**
 * Initialization data for the jupyterlab-fileopen extension.
 */
const extension = {
    id: 'jupyterlab-fileopen:plugin',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__.ISettingRegistry],
    autoStart: true,
    activate: (app, factory, settings) => {
        Promise.all([app.restored, settings.load(SETTINGS_ID)]).then(([, setting]) => {
            const widgetFactory = new FileOpenFactory({
                // TODO Translation
                name: 'FileOpen',
                modelName: 'base64',
                fileTypes: ['desktop'],
                defaultFor: ['desktop'],
                preferKernel: false,
                canStartKernel: false
            }, app);
            const extensions = setting.get('extensions').composite;
            app.docRegistry.addWidgetFactory(widgetFactory);
            app.docRegistry.addFileType({ name: 'desktop', extensions });
            app.docRegistry.setDefaultWidgetFactory('desktop', 'FileOpen');
        });
        app.commands.addCommand(CommandIDs.openFileExplorer, {
            execute: () => {
                const widget = factory.tracker.currentWidget;
                if (widget) {
                    const selection = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.toArray)(widget.selectedItems());
                    if (selection.length !== 1) {
                        return;
                    }
                    const selected = selection[0];
                    const path = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.dirname(selected.path);
                    (0,_handler__WEBPACK_IMPORTED_MODULE_7__.requestAPI)('open-file-explorer', {
                        method: 'POST',
                        body: JSON.stringify({ path: path })
                    })
                        .then(data => {
                        // Was a success
                    })
                        .catch(reason => {
                        console.error(`The jupyterlab-fileopen server extension appears to be missing.\n${reason}`);
                    });
                }
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.folderIcon,
            // TODO Translation
            // label: trans.__('Reveal In File Explorer')
            label: 'Reveal In File Explorer'
        });
        app.commands.addCommand(CommandIDs.openFile, {
            execute: () => {
                const widget = factory.tracker.currentWidget;
                if (widget) {
                    const selection = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.toArray)(widget.selectedItems());
                    if (selection.length !== 1) {
                        return;
                    }
                    const selected = selection[0];
                    (0,_handler__WEBPACK_IMPORTED_MODULE_7__.requestAPI)('open-file', {
                        method: 'POST',
                        body: JSON.stringify({ path: selected.path })
                    })
                        .then(data => {
                        // Was a success
                    })
                        .catch(reason => {
                        console.error(`The jupyterlab-fileopen server extension appears to be missing.\n${reason}`);
                    });
                }
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.folderIcon,
            // TODO Translation
            // label: trans.__('Open With Desktop Application')
            label: 'Open With Desktop Application'
        });
        app.contextMenu.addItem({
            command: CommandIDs.openFileExplorer,
            selector: selectorItem,
            rank: 2
        });
        app.contextMenu.addItem({
            command: CommandIDs.openFile,
            selector: selectorNotDir,
            rank: 2
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.7c6e7936383a7e36d2d3.js.map