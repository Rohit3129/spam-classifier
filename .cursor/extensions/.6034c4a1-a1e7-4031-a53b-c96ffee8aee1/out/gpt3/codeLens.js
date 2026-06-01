"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.CodelensProvider = exports.curDocument = void 0;
exports.setCurDocument = setCurDocument;
exports.ensureChatProvider = ensureChatProvider;
const vscode = __importStar(require("vscode"));
const projectUtils_1 = require("../utils/projectUtils");
const extension_1 = require("../extension");
const commands_1 = require("./commands");
const astDetector_1 = require("./astDetector");
const chatGpt4Provider_1 = require("../chatGPT4/chatGpt4Provider");
const extension_2 = require("../extension");
/**
 * CodelensProvider
 */
function setCurDocument(doc) {
    exports.curDocument = doc;
}
class CodelensProvider {
    constructor() {
        this.codeLenses = [];
        this._onDidChangeCodeLenses = new vscode.EventEmitter();
        this.onDidChangeCodeLenses = this._onDidChangeCodeLenses.event;
        this.jsonSet = [];
        this.funNamesLinesSet = new Set();
        this.funNamesSet = new Set();
        this.curCodeLensDoc = [];
        this.ast = new astDetector_1.AstDetector(exports.curDocument.fileName, exports.curDocument.getText(), "DETECT_AST");
        this.ast.generateAst();
        this.createFileSenderConnector((0, extension_1.getExtensionContext)());
        this.createASTFileListener();
    }
    createASTFileListener() {
        if (this.ast !== null) {
            this.ast.generateAst();
            //console.log("Got file from backend ", json["flag"], this.ws.url);
            if (this.ast.getFlag() === "DETECT_AST") {
                var functions = this.ast.getFunctions();
                let classes = this.ast.getClasses();
                for (let key in classes) {
                    if (classes.hasOwnProperty(key)) {
                        functions = functions.concat(classes[key]["functions"]);
                    }
                }
                if (functions) {
                    //console.log("Got file from backend ", json["flag"], " lenght of functions is ", functions.length);
                    functions.forEach((item) => {
                        //copy codeLens to Set
                        try {
                            item["filename"] = this.ast.getFilename();
                            this.jsonSet.push(item);
                            this.funNamesLinesSet.add(item.startLine);
                            this.funNamesSet.add(item.name);
                        }
                        catch (e) {
                        }
                    });
                }
                //console.log("let's have it",this.jsonSet);
                this.jsonSet.forEach((item) => {
                    const range = new vscode.Range(item.startLine - 1, 0, item.endLine - 1, 0);
                    //console.log("let's have it now",range);
                    this.codeLenses.push(new vscode.CodeLens(range, {
                        title: "Debug this code",
                        tooltip: "Click here to debug and fix the broken part of this function",
                        command: commands_1.DETECT_VULNERABILITY_V2,
                        arguments: [item, false, async () => {
                                const provider = await this.ensureChatProvider();
                                provider.webview?.postMessage({
                                    command: "special_chat_with_user",
                                    value: {
                                        id: Date.now().toString(),
                                        user_prompt: "/fix_code",
                                        code: item.code
                                    }
                                });
                            }]
                    }));
                    this.codeLenses.push(new vscode.CodeLens(range, {
                        title: "Explain this function to me",
                        tooltip: "You don't understand what this code does anymore? Don't stress, just click this button",
                        command: commands_1.EXPLAIN_CODE,
                        arguments: [item, false, async () => {
                                const provider = await this.ensureChatProvider();
                                provider.webview?.postMessage({
                                    command: "special_chat_with_user",
                                    value: {
                                        id: Date.now().toString(),
                                        user_prompt: "/explain_code",
                                        code: item.code
                                    }
                                });
                            }]
                    }));
                    this.codeLenses.push(new vscode.CodeLens(range, {
                        title: "Optimize this function's Speed",
                        tooltip: "This code takes forever to run? Let ChatGPT4 decrease the space and time complexity of this code for you! ",
                        command: commands_1.OPTIMIZE_CODE,
                        arguments: [item, false]
                    }));
                    this.codeLenses.push(new vscode.CodeLens(range, {
                        title: "Generate Doc String",
                        tooltip: "Don't stress yourself generating doc strings anymore, just click this button",
                        command: commands_1.GENERATE_DOC_STRING,
                        arguments: [item, false]
                    }));
                    this.codeLenses.push(new vscode.CodeLens(range, {
                        title: "Generate Unit test",
                        tooltip: "Unit tests shouldn't take much of your time!, don't let it either!",
                        command: commands_1.GENERATE_UNIT_TEST,
                        arguments: [item, false]
                    }));
                });
                var docCodeLens = this.curCodeLensDoc.filter(codelens => codelens.fileName === this.ast.getFilename());
                if (docCodeLens.length > 0) {
                    //delete previous codelens
                    this.curCodeLensDoc = this.curCodeLensDoc.filter(codelens => codelens.fileName !== this.ast.getFilename());
                    this.curCodeLensDoc.push({
                        fileName: this.ast.getFilename(),
                        codeLenses: this.codeLenses
                    });
                }
                else {
                    this.curCodeLensDoc.push({
                        fileName: this.ast.getFilename(),
                        codeLenses: this.codeLenses
                    });
                }
                this.jsonSet = [];
                this.codeLenses = [];
                this._onDidChangeCodeLenses.fire();
            }
        }
    }
    createFileSenderConnector(context) {
        let timer;
        //this.syncDocument();
        vscode.workspace.onDidChangeTextDocument((e) => {
            if (e) {
                exports.curDocument = e.document;
            }
            this.syncDocument();
        });
    }
    syncDocument() {
        const editor = vscode.window.activeTextEditor;
        var apiKey;
        const realApikey = (0, projectUtils_1.getDataFromCache)((0, extension_1.getExtensionContext)(), projectUtils_1.APIKEY, "");
        const tempApikey = (0, projectUtils_1.getDataFromCache)((0, extension_1.getExtensionContext)(), projectUtils_1.TEMP_APIKEY, "");
        if (realApikey) {
            apiKey = realApikey;
        }
        else {
            apiKey = tempApikey;
        }
        if (editor) {
            var curDocument = editor.document;
            if (curDocument && curDocument.fileName.endsWith("py")
                || curDocument.fileName.endsWith("js")
                || curDocument.fileName.endsWith("jsx")
                || curDocument.fileName.endsWith("go")
                || curDocument.fileName.endsWith("ts")
                || curDocument.fileName.endsWith("tsx")
                || curDocument.fileName.endsWith("php")
                || curDocument.fileName.endsWith("php3")
                || curDocument.fileName.endsWith("php4")
                || curDocument.fileName.endsWith("php5")
                || curDocument.fileName.endsWith("inc")) {
                this.ast.reset();
                this.ast.setFlag("DETECT_AST");
                this.ast.setFilename(curDocument.fileName);
                this.ast.setCode(curDocument.getText());
                this.ast.generateAst();
                this.createASTFileListener();
            }
        }
    }
    provideCodeLenses(document, token) {
        if (vscode.workspace.getConfiguration("codelens-sample").get("enableCodeLens", true)) {
            var docCodeLens = this.curCodeLensDoc.filter(codelens => codelens.fileName === document.fileName);
            if (docCodeLens) {
                if (docCodeLens !== undefined) {
                    var res = docCodeLens[docCodeLens.length - 1];
                    if (res) {
                        if (res !== undefined) {
                            return res.codeLenses;
                        }
                        else {
                            return [];
                        }
                    }
                    else {
                        return [];
                    }
                }
                else {
                    return [];
                }
            }
            else {
                return [];
            }
        }
        return [];
    }
    resolveCodeLens(codeLens, token) {
        return codeLens;
    }
    async ensureChatProvider() {
        let provider = extension_2.chatGPT4Provider;
        if (!provider) {
            provider = new chatGpt4Provider_1.ChatGPT4Provider(true, null);
            await provider.provideChat();
            (0, extension_2.setChatGPT4Provider)(provider);
        }
        return provider;
    }
}
exports.CodelensProvider = CodelensProvider;
async function ensureChatProvider() {
    let provider = extension_2.chatGPT4Provider;
    console.log("Ensure Chat Provideprovider ", provider);
    if (!provider) {
        provider = new chatGpt4Provider_1.ChatGPT4Provider(true, null);
        await provider.provideChat();
        (0, extension_2.setChatGPT4Provider)(provider);
    }
    return provider;
}
//# sourceMappingURL=codeLens.js.map