# VRC-Haptics-Host
A highly integrated OSC based haptics sever.

# [Original Project](https://github.com/CaiVR/CaiVR-Custom-Haptic-Vest-V1)
## Why?
Credit for hardware, firmware, and software development goes to [CaiVR](https://www.youtube.com/@Cai_VR). This is based off of his haptic suit initial project: [Youtube](https://www.youtube.com/watch?v=NpQyehRNkGo), [Github](https://github.com/CaiVR/CaiVR-Custom-Haptic-Vest-V1)

I made a vest following CaiVR's original tutorial loosely and have made some changes/improvements to both the server and hardware that have been useful in-game and would like to share them. CaiVR does not wish to further complicate the original project since he is working on something else. [[source]()] So I am going to document/publish my modifications here. **CONTRIBUTIONS ARE WELCOMED**

Please use the Issues tab for any issues with the software. 
Feel free to say hi, although I probably won't be able to respond quickly.
My discord is: @is_average

# Installation
**Not currently Quest Compatible** 

**Prequisites:**
- Any modern Python 3.x version (found here){https://www.python.org/downloads/}
   - **Make sure to check the "Add Python To PATH" box during isntallation**
- This repository 
   - Green button -> "Download ZIP"
   - or `git clone https://github.com/virtuallyaverage/VRC-Haptics-Host.git`

**Installation:**
 - Extract repository into desired install folder.
 - Open a powershell and run: `cd "{Insert file path to unzipped folder}/Server"`
 - Install requirements by running: `pip install -r "requirements.txt"`

Finally, right-click on the `Haptics Server SEND ME TO DESKTOP.lnk` file and select the `"SEND TO"` menu and select `"Desktop"`. This should put the file on the desktop which will start the server when ran. It should also be available from the windows search bar by searching "haptics" or something similar after a computer restart.

**Hardware:**

I am using a mish-mash of components right now, but this is the best arduino based scripts I could find: [Arduino CaiVR Branch](https://github.com/fisk1234ost/CaiVR-Custom-Haptic-Vest-V1)

My current plan is to eventually get a firmware going using platform.io and custom UDP packet setup. But until then the server should support [this](https://github.com/fisk1234ost/CaiVR-Custom-Haptic-Vest-V1) firmware working on almost any wifi enabled chip that can handle i2c, which is some arduino and most esp32/esp8 chips. (I a using a D1 Mini)

I have custom cases/modules designed on onshape and will share the .STL and links to that once I am sure they somewhat function.

**Game Integration:**

The asset provided by CaiVR is NOT COMPATIBLE with this server. I had to modify some of the addresses that his prefab uses to prevent some parameter clashes.

In the Unity folder is the Haptics Prefab that includes both a full PC and a quest version that only shows the collider placement. VRCFURY is used to integrate the menus and avatar placement. It should be as simple as importing vrcfury and dragging a prefab onto the base of the avatar and uploading. 

# Contributors
 **Submit litterally anything *that gets merged* and get your name here**
 
 **YES, A SINGLE DOCSTRING WILL GET A NAME HERE** 

# Goals
## Long-Time Goals
 - More App support
 - Improved VRC Integration
 - Live Configuration
 - Better Error handling
 - Working UI
 - Automatic Unity Installer
 - Modular Structure
 - Custom/Easy Feedback Configurations

## Current Areas of Improvment:
My time for this project is very limited at the moment since I work 60-70hrs a week and have medical issues. ANY little thing helps, even if it is just reordering what is already there. Anyone willing to write good(readable) documentation for the project is worth their weight in gold to me. 

I will accept well curated AI generations, please denote when one is used significantly though.
There are ALOT of areas that need improvement immediately. The current codebase is a wreck, there is no proper scope management, and I kind of scattered functions willy-nilly during initial developement. 
 
### Urgent-ish needs:
   - Major Refactoring
      - split out functions to their own modules
      - implement object based scope management (remove global variables entirely)
      - document functions/objects
   - Start code docs 
      - The goal is to have a properly formatted docstring on each function added to the main repository.
   - Create Platform.io project
      - Same documentation standards as the server. 
      - IF you make your own repository PLEASE LET ME KNOW AND YOU WILL GET LINKED ON HERE. 


# Design Principles
Contribution is more than appreciated, but please keep it close/aligned with the projects over all goals:
 - Robust 
    - not many "hacky" work arounds
    - feel free to open a branch or your own fork if you would like to work in collaboration before merging to main
 - Simple To set up 
    - users shouldn't have to spend half an hour downloading python dependencies, something similar to AUTOMATIC's Stable Diffusion is the goal. 
 - Follow common Python syntax, such as snake case variables (variable_name)
 - **Readable Code** 
    - I would prefer having slightly less performant code if it is easily understandable. 
    - Please avoid ambigous variable naming (temp, i, j, etc.)

If the project takes off than rules and goals can change as needed. These are just general guidelines to start off. 

