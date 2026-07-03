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
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const fs = __importStar(require("fs"));
function extractPythonFunction(document, cursorLine) {
    let functionStart = -1;
    //to search upward
    for (let i = cursorLine; i >= 0; i--) {
        const line = document.lineAt(i).text;
        const trimmed = line.trim();
        if (trimmed.startsWith("def ") || trimmed.startsWith("class ")) {
            functionStart = i;
            break;
        }
    }
    if (functionStart === -1) {
        return "No function found";
    }
    //to get where the function starts and how many lines are there before the function to know indentation
    const startText = document.lineAt(functionStart).text;
    const functionIndent = startText.length - startText.trimStart().length;
    let functionText = "";
    //Extract until indentation drops
    for (let i = functionStart; i < document.lineCount; i++) {
        const line = document.lineAt(i).text;
        const trimmed = line.trim();
        //this checks for indentation of the function if it is less then the indentation it breaks
        if (i > functionStart && trimmed !== "") {
            const currentIndent = line.length - line.trimStart().length;
            if (currentIndent <= functionIndent) {
                break;
            }
        }
        functionText += line + "\n";
    }
    return functionText;
}
function activate(context) {
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
        const endLine = Math.min(document.lineCount - 1, cursorLine + 3);
        let nearbyCode = "";
        for (let i = startLine; i <= endLine; i++) {
            nearbyCode += document.lineAt(i).text + "\n";
        }
        console.log({
            file: fileName,
            line: cursorLine,
            nearbyCode: nearbyCode,
            functionContext: functionContext
        });
        const contextData = {
            file: fileName,
            line: cursorLine,
            nearbyCode: nearbyCode,
            functionContext: functionContext
        };
        const contextPath = "C:\\Users\\novac\\OneDrive\\Desktop\\Ai\\vscode_context.json";
        //fs=node.js
        fs.writeFileSync(//Write data to a file immediately (synchronously).
        contextPath, JSON.stringify(contextData, null, 2));
        console.log(contextData);
    }
    logEditorContext();
    const selectionListener = vscode.window.onDidChangeTextEditorSelection(() => {
        logEditorContext();
    });
    context.subscriptions.push(selectionListener);
}
function deactivate() { }
//# sourceMappingURL=extension.js.map