# Package Reloader

A simple reloader to manage the reload process of dependency modules in Sublime Text. The package reloads changes of a class while developing a plugin on the fly without restarting Sublime Text.

## Usage

To enable the reload of a certain package you just have to place an empty *.build* file inside the package directory. You do not have to fill the file by yourself, just save a file inside the plugin and Package Reloader will fill all the basic informations. You can adjust the loading order with **mods_load_order** after the first run. After the first run (save of a file in that project) `.build` could look like this:

	{
		"automatic_order": true,
		"iterations": 1,
		"mods_load_order":
		[
			"File Navigator.py",
			"file_navigator/__init__.py",
			"file_navigator/tools.py"
		]
	}

The **automatic_order** can true or false, if you are using true the order will be automatically arranged every time you are adding a new source file. If you are using false, the new item will be just add the end of the list and you can change that on your own. If you for example need to load the *file_navigator/tools.py* before *File Navigator.py* just change the *.build* like this:

	{
		"automatic_order": false,
		"iterations": 1,
		"mods_load_order":
		[
			"file_navigator/tools.py",
			"File Navigator.py",
			"file_navigator/__init__.py"
		]
	}

## Installation

### Using Package Control:

* Bring up the Command Palette (Command+Shift+P on OS X, Control+Shift+P on Linux/Windows).
* Select Package Control: Install Package.
* Select Package Reloader to install.

### Not using Package Control:

* Save files to the `Packages/Package Reloader` directory, then relaunch Sublime:
  * Linux: `~/.config/sublime-text-2|3/Packages/Package Reloader`
  * Mac: `~/Library/Application Support/Sublime Text 2|3/Packages/Package Reloader`
  * Windows: `%APPDATA%/Sublime Text 2|3/Packages/Package Reloader`

## Donating

Support this project via [gittip][] or [paypal][].

[![Support via Gittip](https://rawgithub.com/chris---/Donation-Badges/master/gittip.jpeg)][gittip] [![Support via PayPal](https://rawgithub.com/chris---/Donation-Badges/master/paypal.jpeg)][paypal]

[gittip]: https://www.gittip.com/Chris---
[paypal]: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ZWZCJPFSZNXEW

## License

All files in this package is licensed under the MIT license.

Copyright (c) 2013 Chris <chris@latexing.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.