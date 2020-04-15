<p align="center">
  <img src="https://github.com/kitchensjn/TopoTable/blob/master/TopoTableLogo.png" width="200" height="197">
</p>

The TopoTable Project focuses around the development of a raised relief map table made of moveable pillars, allowing the user to display many custom elevation maps. By doing this, I hope to bridge the gap between physical maps, which are tactile but generally static, and digital maps. The TopoTable has potential as an educational tool in a GIS classroom or museum, as well as a decorative piece (similar to a kinetic sculpture).

Files within this directory relate to development of a software workflow for converting maps into useable formats for the table and, ultimately, map display. Descriptions of the files found in this respository are found below:

# Shiny Application

Hosted through shinyapps.io at [jkitchensf16.shinyapps.io/topotable](https://jkitchensf16.shinyapps.io/topotable), this is the most streamlined version of the application to date. Users can select a region of the word to download, including location and size, and download the respective raster from Amazon Web Services (AWS). This is conviently simple thanks to the elevatr package in R. The user can pick the number of pillars that make up their table and the physical size of each pillar (width/height). The application displays a preview of what your TopoTable will look like, and finally, if the user likes their selection, they can download the map as a .csv file which will be fed into the TopoTable.

# Desktop Application

The desktop application is Python code that has been converted into an executable for OSX and Windows. This is an older version of the application and for individuals who want to use custom maps rather than those pulled from AWS. In general, I would recommend trying the Shiny Application first before downloading and installing a version of the desktop application.

## Source Files and Previous Versions

### Deprecated Versions
This folder contains all of the deprecated versions of the GUI that I have created. These versions should still function, but may not directly follow current instructions and/or lack certain features. For most recent versions of the GUI, see below.

### Pixelate and Scale Map
Backend of the map conversion. This code communicates with the GUI used to take maps downloaded from 'terrain.party' and produce a .csv file with associated heights of each pillar to display map to scale. In doing so, the program takes the higher resolution map and pixelates it to the resolution expected by the table. Grayscale values (elevation values) rescaled to the pillar heights based on the footprints of the original map and tables. File is saved in the directory of original maps.

### PyQt GUI
Frontend of the map conversion. This code communicates with the backend program used to take maps downloaded from 'terrain.party' and produce a '.csv' file with associated heights of each pillar to display map to scale. Running this code opens a new window with inputs used to set parameters for backend.

## TopoTable for Windows and TopoTable for OSX
These are standalone applications created from the Python source files using pyinstaller. These applications should be able to run without other dependencies, acting as the most streamline way of using the program. **The latest version of TopoTable for Windows does not have a formatted GUI yet, but functionality should still be the same! (09/05/2019)**

### Instructions for Using These Applications
1. Go to **'terrain.party'**
2. Find a region that you like, note the **footprint size of the region**, and click the button with a **cloud and downward arrow** to download
3. Run the **TopoTable for [operating system]** application
4. **Browse** to the region directory that you just downloaded and click open
5. Enter in the **footprint size** of your region in meters, leaving off the units
6. Enter in the **number of pillars** that make up one dimension of your table (10 pillar x 10 pillar table = 10)
7. Enter in the **width of each pillar** in centimeters, leaving off units
8. The program will produce two files:
- A **pixelated map** of the region corresponding to the number of pillars in your table 
- A **pillar position file** containing the heights of all of the pillars

#
I am currently seeking advice for how to bring this project into the next stages of development, including design and fabrication of a physical prototype. For information or questions about the project, feel free to contact me (**James Kitchens**) at kitchensjn@gmail.com.

**Disclaimer: This project is not affiliated with 'terrain.party' in any way and only uses the website as it is an easy and consistent way of finding maps for many regions of the world.**

## Updates
****UPDATE 03/01/2020 : I am currently working to create a web application that will ultimately replace the standalone application described above. This application will be created through the Shiny package in R, which I used for a previous project (see marine-tardigrades repository). You will be able to find code for this new direction within the "Shiny Application" directory****

****UPDATE 04/15/2020 : I have completed a basic version of the Shiny Web Application. Source files can be found within the "Shiny Application" directory. I decided to rewrite the backend functionality in R (rather than Python) so that it pairs more easily with Shiny. I found a set of packages that work well with geospatial data (raster, sp, rgdal, elevatr)****
