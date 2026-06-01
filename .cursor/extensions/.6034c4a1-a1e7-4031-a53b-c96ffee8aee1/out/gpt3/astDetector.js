"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AstDetector = void 0;
const { parseGOCode } = require("../utils/astUtils/goAstUtils");
const { parseJavascriptCode } = require("../utils/astUtils/javascriptAstUtils");
const { parsePhpCode } = require("../utils/astUtils/phpAstUtils");
const { parsePythonCode } = require("../utils/astUtils/pythonAstUtils");
const { parseTypescriptCode } = require("../utils/astUtils/typescriptAstUtils");
class AstDetector {
    constructor(filename, code, flag) {
        this.functions = [];
        this.classes = {};
        this.code = "";
        this.filename = filename;
        this.code = code;
        this.flag = flag;
    }
    setFunction(newFunctions) {
        this.functions = newFunctions;
    }
    setClass(newClasses) {
        this.classes = newClasses;
    }
    setFilename(filename) {
        this.filename = filename;
    }
    setFlag(flag) {
        this.flag = flag;
    }
    setCode(code) {
        this.code = code;
    }
    getFunctions() {
        return this.functions;
    }
    getClasses() {
        return this.classes;
    }
    getFilename() {
        return this.filename;
    }
    getFlag() {
        return this.flag;
    }
    reset() {
        this.functions = [];
        this.classes = {};
        this.filename = '';
        this.code = '';
    }
    generateAst() {
        if (this.filename.endsWith(".git")) {
            this.setFilename(this.filename.replace(".git", ""));
        }
        let results = {};
        if (this.filename.endsWith("js") || this.filename.endsWith("jsx")) {
            try {
                results = parseJavascriptCode(this.code);
            }
            catch (e) {
            }
        }
        else if (this.filename.endsWith("go")) {
            try {
                results = parseGOCode(this.code);
            }
            catch (e) {
            }
        }
        else if (this.filename.endsWith("py")) {
            try {
                results = parsePythonCode(this.code);
            }
            catch (e) {
            }
        }
        else if (this.filename.endsWith("php3") || this.filename.endsWith("php4") || this.filename.endsWith("php5") || this.filename.endsWith("php")) {
            try {
                results = parsePhpCode(this.code);
            }
            catch (e) {
            }
        }
        else if (this.filename.endsWith("ts") || this.filename.endsWith("tsx")) {
            try {
                results = parseTypescriptCode(this.code);
            }
            catch (e) {
            }
        }
        if (results) {
            this.functions = results["functions"];
            this.classes = results["classes"];
            try {
                if (Object.keys(this.classes).length === 0 && this.functions.length === 0 && this.code.length > 1) {
                    this.generateAst();
                }
            }
            catch {
            }
        }
        else {
            this.functions = [];
            this.classes = {};
        }
    }
}
exports.AstDetector = AstDetector;
//# sourceMappingURL=astDetector.js.map