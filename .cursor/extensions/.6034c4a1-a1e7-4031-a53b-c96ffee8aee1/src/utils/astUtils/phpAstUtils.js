const parser = require('php-parser');

const phpParser = new parser({
    // some options :
    // https://github.com/glayzzle/php-parser#parser-options
    // default options :
    parser: {
      extractDoc: true,
      php7: true
    },
    ast: {
      withPositions: true
    }
  });

  function parsePhpCode(code){

    const functions = [];
    const classes = {};

    const tree = phpParser.parseCode(code, 'code.php');

    tree.children.forEach(node => {
        if (node.kind === 'class') {
            const classInfo = extractClasses(node, code);
            classes[classInfo.name] = classInfo;
        } else if (node.kind === 'function') {
            const functionInfo = extractFunctions(node, code);
            functions.push(functionInfo);
        } else if(node.kind==="expressionstatement"){
            if(node.expression!==null){
                if(node.expression.right!==null&& node.expression.right !== undefined){
                    if(node.expression.right.kind==="closure"){
                        functions.push(extractAnonymousFunction(node,code));
                        

                    }
                }
            }
        }
    });

    
    return { functions, classes };
  }

  function extractFunctions(node, code) {
    const name=node.name.name;
    const startLine=node.loc.start.line;
    const endLine=node.loc.end.line;
    const functionCode = code.substring(node.loc.start.offset, node.loc.end.offset);

    return {
        type: "func",
        name,
        code: functionCode,
        startLine,
        endLine,
    };
}

function extractAnonymousFunction(node,code){
    const name=node.expression.left.name;
    const startLine=node.loc.start.line;
    const endLine=node.loc.end.line;
    const functionCode = code.substring(node.loc.start.offset, node.loc.end.offset);
    return {
        type: "func",
        name,
        code: functionCode,
        startLine,
        endLine,
    };
}

function extractClasses(node, code) {
    const name=node.name.name;
    const startLine=node.loc.start.line;
    const endLine=node.loc.end.line;
    const functions = [];

    node.body.forEach(child=>{
        if(child.kind==="method"){
            functions.push(extractFunctions(child,code));
        }
    });

    

    const classCode = code.substring(node.loc.start.offset, node.loc.end.offset);

    return {
        type: "class",
        name,
        code: classCode,
        startLine,
        endLine,
        functions,
    };
}

// Export the function for CommonJS
module.exports = { parsePhpCode };