# Package Reloader

A simple reloader to manage the reload process while developing your own plugin for Sublime Text.

## Usage

To enable the reload of a certain package you have to place an empty *.build* file inside the package directory. You do not have to fill the file by yourself, you can just adjust the **mods_load_order**. Package Reloader will fill this file automatically, after the first run it could look like this:

	{
		"mods_load_order":
		[
			"File Navigator.Tools",
			"File Navigator.File Navigator",
			"File Navigator"
		],
		"manual_order": false
	}

The **automatic_order** can true or false, if you are using true the order will be automatically arranged every time you are adding a new source file in inverse order. If you are using false, the new item will be just add the end of the list. If you for example need to load *File Navigator.File Navigator* before *File Navigator.Tools* change the *.build* like this:

	{
		"mods_load_order":
		[
			"File Navigator.File Navigator",
			"File Navigator.Tools",
			"File Navigator"
		],
		"manual_order": true
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

[![Support via Gittip](https://rawgithub.com/chris---/Donation-Badges/master/gittip.jpeg)][gittip]
[![Support via PayPal](https://rawgithub.com/chris---/Donation-Badges/master/paypal.jpeg)][paypal]

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