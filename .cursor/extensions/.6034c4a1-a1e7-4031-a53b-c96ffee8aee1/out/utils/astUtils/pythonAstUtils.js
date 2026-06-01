const Parser  = require('tree-sitter');
const Python = require('tree-sitter-python');


const parser = new Parser();
const language = Python;
//console.log(language,typeof language.language,"see");




function parsePythonCode(code) {
    const functions = [];
    const classes = {};
    try{
      parser.setLanguage(language);
      const tree = parser.parse(code);
      
      
      // Traverse the tree and collect function and class information
    for (const node of tree.rootNode.children) {
      if (node.type === "function_definition") {
        const functionInfo = extractFunctionInfo(node, code);
        functions.push(functionInfo);
      } else if (node.type === "class_definition") {
        const classInfo = extractClassInfo(node, code);
        classes[classInfo.name] = classInfo;
      } else if(node.type==="decorated_definition"){
        const functionInfo = extractDecoratedFunctionInfo(node, code);
        functions.push(functionInfo);
      }

      
    }
    }catch(e){

    }
  return { functions, classes };
}

function extractDecoratedFunctionInfo(node,code){
  let name='';
  let functionNode=null;
  for (const child of node.children) {
    if (child.type === "function_definition") {
      functionNode=child;
      for(const childChild of child.children){
        if (childChild.type === "identifier") {
          name = childChild.text;
          
        }
      }
    const startLine = node.startPosition.row;
    const endLine = functionNode.endPosition.row;
    const functionCode = code.substring(node.startIndex, functionNode.endIndex);
    return {
      type: "func",
      name,
      code: functionCode,
      startLine: startLine+1,
      endLine: endLine+1,
    };
    }
  }
}

function extractFunctionInfo(node, code) {
    let name = '';
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
      startLine: startLine+1,
      endLine: endLine+1,
    };
  }

  function extractClassInfo(node, code) {
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
      if (child.type === "block") {
        
        for(const funcs of child.children){
            if(funcs.type==="function_definition"){
                const functionInfo = extractFunctionInfo(funcs, code);
                functions.push(functionInfo);
            }
        }
      }
    }
  
    return {
      type: "class",
      name,
      code: classCode,
      startLine: startLine+1,
      endLine: endLine+1,
      functions,
    };
  }

  // Export the function for CommonJS
module.exports = { parsePythonCode };
  
