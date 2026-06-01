const Parser = require('tree-sitter');
const Javscript = require('tree-sitter-javascript');

const parser = new Parser();
const language = Javscript;

function parseJavascriptCode(code) {
    const functions = [];
    const classes = {};

    parser.setLanguage(language);
    const tree = parser.parse(code);

    for (const node of tree.rootNode.children) {
        if (node.type === "function_declaration") {
            const functionInfo = extractFunctions(node, code, false);
            functions.push(functionInfo);
        } else if (node.type === "class_declaration") {
            const classInfo = extractClasses(node, code);
            classes[classInfo.name] = classInfo;
        } else if (node.type === "lexical_declaration") {
            const cursor = node;
            for (const cursorChild of cursor.children) {
                if (cursorChild.type === "variable_declarator") {
                    for (const cursorChildChild of cursorChild.children) {
                        if (cursorChildChild.type === "arrow_function") {
                            const functionInfo = extractFunctions(node, code, true);
                            functions.push(functionInfo);
                        }
                    }
                }
            }
        }
    }

    return { functions, classes };
}

function extractFunctions(node, code, arrowFunction = false) {
    let name = '';
    if (arrowFunction === false) {
        for (const child of node.children) {
            if (child.type === "identifier") {
                name = child.text;
                break;
            }
        }
        const startLine = node.startPosition.row;
        const endLine = node.endPosition.row;

        const functionCode = code.substring(node.startIndex, node.endIndex);

        return {
            type: "func",
            name,
            code: functionCode,
            startLine: startLine + 1,
            endLine: endLine + 1,
        };

    } else {
        for (const child of node.children) {
            if (child.type === "variable_declarator") {
                for (const innerChild of child.children) {
                    if (innerChild.type === "identifier") {
                        name = innerChild.text;
                        break;
                    }
                }
            }
        }
        const startLine = node.startPosition.row;
        const endLine = node.endPosition.row;

        const functionCode = code.substring(node.startIndex, node.endIndex);

        return {
            type: "func",
            name,
            code: functionCode,
            startLine: startLine + 1,
            endLine: endLine + 1,
        };
    }
}

function extractClassMethods(node, code) {
    let name = '';
    for (const child of node.children) {
        if (child.type === "property_identifier") {
            name = child.text;
            break;
        }
    }

    const startLine = node.startPosition.row;
    const endLine = node.endPosition.row;

    const functionCode = code.substring(node.startIndex, node.endIndex);

    return {
        type: "func",
        name,
        code: functionCode,
        startLine: startLine + 1,
        endLine: endLine + 1,
    };
}

function extractClasses(node, code) {
    let name = '';
    for (const child of node.children) {
        if (child.type === "identifier") {
            name = child.text;
            break;
        }
    }

    const startLine = node.startPosition.row;
    const endLine = node.endPosition.row;

    const classCode = code.substring(node.startIndex, node.endIndex);

    const functions = [];

    for (const child of node.children) {
        if (child.type === "class_body") {
            for (const funcs of child.children) {
                if (funcs.type === "method_definition") {
                    for (const funcChild of funcs.children) {
                        if (funcChild.type === "property_identifier") {
                            if (funcChild.text !== "constructor") {
                                const functionInfo = extractClassMethods(funcs, code);
                                functions.push(functionInfo);
                            }
                        }
                    }
                }
            }
        }
    }

    return {
        type: "class",
        name,
        code: classCode,
        startLine: startLine + 1,
        endLine: endLine + 1,
        functions,
    };
}

// Export the function for CommonJS
module.exports = { parseJavascriptCode };