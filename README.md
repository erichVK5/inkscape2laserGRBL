Simple GRBL G-Code Output for Inkscape targeting laser cutters
==============================================================

Notice
------

This is an Inkscape extension that allows you to save paths in Inkscape as
G-Code suitable for plotting with inexpensive laser cutters running GRBL.

**this extension has been tested on a cheap ebay laser cutter running GRBL 0.8c.
Users exporting gcode for other devices do so at their own risk.**

Author: [Erich S. Heinzle](http://github.com/erichVK5/)

Website: [http://github.com/erichVK5/inkscape2laserGRBL](http://github.com/erichVK5/inkscape2laserGRBL)

Credits
=======

* [Marty McGuire](http://github.com/martymcguire) created an Inkscape extension for the Makerbot Unicorn, from which this code is derived.
* [Inkscape](http://www.inkscape.org/) is basically _the_ open source vector graphics application.
* [Scribbles](https://github.com/makerbot/Makerbot/tree/master/Unicorn/Scribbles%20Scripts) is the original DXF-to-Unicorn Python script.

Install
=======

Copy the contents of `src/` to your Inkscape `extensions/` folder.

Typical locations include:

* OS X - `/Applications/Inkscape.app/Contents/Resources/extensions`
* Linux - `/usr/share/inkscape/extensions`
* Windows - `C:\Program Files\Inkscape\share\extensions`

Usage
=====

* Size and locate your image appropriately:
	* The CupCake CNC build platform size is 100mm x 100mm.
	* Setting units to **mm** in Inkscape makes it easy to size your drawing.
	* The extension will automatically attempt to center everything.
* Convert all text to paths:
	* Select all text objects.
	* Choose **Path | Object to Path**.
* Save as G-Code:
	* **File | Save a Copy**.
	* Select **MakerBot Unicorn G-Code (\*.gcode)**.
	* Save your file.
* Preview
	* [Universal gcode Sender](https://winder.github.io/ugs_website/) is a cross platform java application that also allows visualisation.
	* Plenty of other visualisation options exist too
* Burn baby burn!
	* Open your `.gcode` file in [Universal gcode Sender](https://winder.github.io/ugs_website/)
	* Position the laser in the gantry appropriately.
	* Shield yourself from direct and reflected laser light, and/or wear suitable laser goggles.
	* Click the **Send** button!

TODOs
=====

* Rename `*PolyLine` stuff to `*Path` to be less misleading.
* Parameterize smoothness for curve approximation.
* Use native curve G-Codes instead of converting to paths?
