import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
function extractPythonFunction(document: vscode.TextDocument, cursorLine: number){
	let functionStart=-1;
	//to search upward
	for(let i=cursorLine;i>=0;i--)
	{
		const line=document.lineAt(i).text;
		const trimmed=line.trim();
		if(trimmed.startsWith("def ")|| trimmed.startsWith("class "))
		{
			functionStart=i;
			break;
		}
	}
	if(functionStart===-1)
	{
		return "No function found";
	}
	//to get where the function starts and how many lines are there before the function to know indentation
	const startText = document.lineAt(functionStart).text;
	const functionIndent=startText.length-startText.trimStart().length;
	let functionText="";
	//Extract until indentation drops
	for(let i=functionStart;i<document.lineCount;i++)
	{
		const line=document.lineAt(i).text;
		const trimmed=line.trim();
		//this checks for indentation of the function if it is less then the indentation it breaks
		if (i > functionStart && trimmed !== "") {
			const currentIndent =
				line.length - line.trimStart().length;
			if (currentIndent <= functionIndent) {
				break;
			}
		}
		functionText+=line+"\n";
	}
	return functionText;
}
export function activate(context: vscode.ExtensionContext) {
	vscode.window.showInformationMessage("Extension activated!");
	console.log('Personal Context extension active!');
	function logEditorContext() {
		const editor = vscode.window.activeTextEditor;
		if (!editor) {
			console.log("No active editor");
			return;
		}
		const document = editor.document;
		const fileName = document.fileName;
		const cursorLine = editor.selection.active.line;
		const functionContext = extractPythonFunction(document, cursorLine);
		const startLine = Math.max(0, cursorLine - 3);
		const endLine = Math.min(
			document.lineCount - 1,
			cursorLine + 3
		);
		let nearbyCode = "";
		for (let i = startLine; i <= endLine; i++) {
			nearbyCode += document.lineAt(i).text + "\n";
		}
		console.log({
			file: fileName,
			line: cursorLine,
			nearbyCode: nearbyCode,
			functionContext:functionContext
		});
		const contextData = {
	file: fileName,
	line: cursorLine,
	nearbyCode: nearbyCode,
	functionContext: functionContext
};
const contextPath =
	"C:\\Users\\novac\\OneDrive\\Desktop\\Ai\\vscode_context.json";
	//fs=node.js
fs.writeFileSync(//Write data to a file immediately (synchronously).
	contextPath,
	JSON.stringify(contextData, null, 2)
);
console.log(contextData);
	}
	logEditorContext();
	const selectionListener =
		vscode.window.onDidChangeTextEditorSelection(() => {
			logEditorContext();
		});
	context.subscriptions.push(selectionListener);
}
export function deactivate() {}