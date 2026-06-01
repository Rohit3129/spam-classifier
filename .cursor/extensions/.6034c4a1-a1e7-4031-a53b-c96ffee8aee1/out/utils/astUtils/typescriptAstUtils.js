const ts = require('typescript');


function parseTypescriptCode(sourceCode) {
    //parseTypescriptCode
    //generateAST
    const sourceFile = ts.createSourceFile(
      'temp.ts',
      sourceCode,
      ts.ScriptTarget.Latest,
      true
    );
  
    return extractFunctionsAndClasses(sourceFile);
  }

  function extractFunctionsAndClasses(sourceFile) {
    const functions = [];
    const classes = {};
  
    function visit(node) {
      if (ts.isFunctionDeclaration(node)) {
        const { name } = node;
        if (name) {
          const startLine = sourceFile.getLineAndCharacterOfPosition(node.getStart()).line + 1;
          const endLine = sourceFile.getLineAndCharacterOfPosition(node.getEnd()).line + 1;
          const code = sourceFile.getText().substring(node.getStart(), node.getEnd());
          functions.push({ name: name.getText(), startLine, endLine, code,type:"func" });
        }
      } else if (ts.isClassDeclaration(node)) {
        const { name } = node;
        if (name) {
          const startLine = sourceFile.getLineAndCharacterOfPosition(node.getStart()).line + 1;
          const endLine = sourceFile.getLineAndCharacterOfPosition(node.getEnd()).line + 1;
          const code = sourceFile.getText().substring(node.getStart(), node.getEnd());
          const methods = [];
          node.members.forEach(member => {
                if (ts.isMethodDeclaration(member)) {
                const methodName = member.name.getText();
                const startLine = sourceFile.getLineAndCharacterOfPosition(member.getStart()).line + 1;
                const endLine = sourceFile.getLineAndCharacterOfPosition(member.getEnd()).line + 1;
                const code = sourceFile.getText().substring(member.getStart(), member.getEnd());
                methods.push({ name: methodName, startLine, endLine, code });
                }
            });
          //classes.push({ name: name.getText(), startLine, endLine, code });
          classes[name.getText()]={"name":name.getText(),"startLine":startLine,"endLine":endLine,"code":code,type:"class","functions":methods};
        }
      }else if (ts.isArrowFunction(node)){
        //const { name } = node;
        if(ts.isVariableStatement(node.parent.parent.parent)){
            const startLine = sourceFile.getLineAndCharacterOfPosition(node.parent.parent.parent.getStart()).line + 1;
            const endLine = sourceFile.getLineAndCharacterOfPosition(node.parent.parent.parent.getEnd()).line + 1;
            const code = sourceFile.getText().substring(node.parent.parent.parent.getStart(), node.parent.parent.parent.getEnd());
            functions.push({ name: node.parent.name.getText(), startLine, endLine, code,type:"func" });
        }
      }
  
      ts.forEachChild(node, visit);
    }
  
    visit(sourceFile);
  
    return { functions, classes };
  }

  // Export the function for CommonJS
module.exports = { parseTypescriptCode };