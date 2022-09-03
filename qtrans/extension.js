// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "qtrans" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('qtrans.fillhole', function () {
		// The code you place here will be executed every time your command is executed
		const express=require('express');
		const app=express();
		
		//Import PythonShell module.
		const {PythonShell} =require('python-shell');
		PythonShell.runString('print(1+1)');
		// Display a message box to the user
		const editor = vscode.window.activeTextEditor;
		const selection = editor.selection;
		if (selection && !selection.isEmpty) {
			const selectionRange = new vscode.Range(selection.start.line, selection.start.character, selection.end.line, selection.end.character);
			const highlighted = editor.document.getText(selectionRange);
			vscode.window.showInformationMessage(highlighted);
			// editor.selections = editor.selections.map( sel => new vscode.Selection(sel.start.translate(0,1), sel.end.translate(0,1)));

			//Here are the option object in which arguments can be passed for the python_test.js.
			// let options = {
			// 	mode: 'text',
			// 	pythonOptions: ['-u'], // get print results in real-time
			// 		//scriptPath: './', //If you are having python_test.py script in same folder, then it's optional.
			// 	args: [__dirname+'\\tmp.txt'] //An argument which can be accessed in the script using sys.argv[1]
			// };
				
			// console.log("start run python")
			// PythonShell.run(__dirname+'\\qtrans.py', options, function (err, result){
					
			// 		if (err) throw err;
			// 		// result is an array consisting of messages collected
			// 		//during execution of script.
			// 		console.log('result: ', result.toString());
			// 		editor.edit(editBuilder => {
			// 			editBuilder.replace(new vscode.Range(editor.selection.start, editor.selection.end), result.toString());
			// 		});
			// });
			
			var fs = require("fs");
			const tmppath = __dirname+'\\tmp.txt';
			fs.writeFile(tmppath, highlighted, function (err) {
				if (err) {
				  return console.error(err);
				}
				const execSync = require('child_process').execSync;
			
				const command = 'python '+__dirname+'\\qtrans.py '+__dirname+'\\tmp.txt';
				console.log(command)
				const output = execSync(command, { encoding: 'utf-8' });  // the default is 'buffer'
				console.log('Output was:\n', output);
				editor.edit(editBuilder => {
					editBuilder.replace(new vscode.Range(editor.selection.start, editor.selection.end), output);
				});
			});

		}
	});

	context.subscriptions.push(disposable);
}

// this method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}
