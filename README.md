# VRC-Haptics-Host
A server and prefab combo prioritizing practical usability and easy customization.
## Features
 - **In-game haptic configuration**
 - **Imperceptable game -> haptics latency**
 - **Cheap Hardware (~$50USD)**
 - **One-Click Avi Install** 
 - **Unlimited Play Time\***
 - **Comfort with custom fitted arrangement**
 - **Eliminate Bhaptics bugs**
 - **Automatic Netowork Discovery**

 *(Support for any Bhaptics equipped avatar coming soon)* 
 
 *\*Unlimited play time provided by fast charge USB power banks and low current haptics*
# Why?
I found [SenseShift](https://github.com/senseshift/senseshift-hardware/tree/main) but was unsatisfied with the bugs present in the bhaptics system for VRC. I also found [CaiVR's Project](https://github.com/CaiVR/CaiVR-Custom-Haptic-Vest-V1), [(Youtube Video)](https://youtu.be/NpQyehRNkGo?si=Qb1jhNKtKzWZTeLw) but he has expressed disinterest in continuing [development itterations](https://github.com/CaiVR/CaiVR-Custom-Haptic-Vest-V1/pull/2). So I started designing a relatively simple Hardware, Firmware, Server, and Prefab stack based on his groundwork but with greatly expanded goals. The stack is in its basic stages but has proven (to me) reliable and simple enough in use. 

Credit for initial hardware, firmware, and software development goes to [CaiVR](https://www.youtube.com/@Cai_VR). His initial development spurred a lot of motivation that got this functional. 

#
Please use the Issues tab for any issues with the software. 
I'll get a discord up eventually. If I dont respond to an issue or you would like to discuss something: 

discord:@is_average


# Installation
**The Server Is Not Currently Quest Compatible** 

**Prequisites:**
- Any modern Python 3.x version: [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - **Make sure to check the "Add Python To PATH" box during isntallation**
- This repository 
   - Green button -> "Download ZIP"
   - or `git clone https://github.com/virtuallyaverage/VRC-Haptics-Host.git`

**Installation:**
 - Extract repository into desired install folder.
 - Open a powershell and run: `cd "{Insert file path to unzipped folder}/VRC-Haptics-Host/Server"`
 - Install requirements by running: `pip install -r "requirements.txt"`

Finally, right-click on the `Haptics Server SEND ME TO DESKTOP.lnk` file and select the `"SEND TO"` menu and select `"Desktop"`. This should put the file on the desktop which will start the server when ran. It should also be available from the windows search bar by searching "haptics" or something similar after a computer restart.

**Hardware:**
No solid versions of hardware are available at this time. I am currently using a very rough alpha setup. [Early Alpha Vest Version](https://github.com/virtuallyaverage/VRC-Haptics-Host/blob/main/img/full_vest_alpha.jpg?raw=true)

**Firmware**: 
See the firmware page: (readme coming soon) [VRC-Haptics-Firmware](https://github.com/virtuallyaverage/VRC-Haptics-Firmware)

The very quickly designed case used in the alpha: [**Onshape Link**](https://cad.onshape.com/documents/257bb1e3453d3517fc7e2da0/w/225abaf7356b023129e9ba7c/e/db6db330ea0d5d698d05a615?renderMode=0&uiState=66c80ae2704979529282d8f5)

**Game Integration:**

The Prefab Uses VRCFury to integrate configuration options into the base of the avatars menu. At any time this prefab can be disabled/deleted without permanantly modifying the avatar at any point. 
[Radial Menu](https://github.com/virtuallyaverage/VRC-Haptics-Host/blob/main/img/radial.png?raw=true)

[Masc Prefab](https://github.com/virtuallyaverage/VRC-Haptics-Host/blob/main/img/masc_prefab.png?raw=true)
[Fem Prefab](https://github.com/virtuallyaverage/VRC-Haptics-Host/blob/main/img/fem_prefab.png?raw=true)

In the Unity folder, the Haptics Prefab includes both a full PC and a quest version that only shows the collider placement. VRCFURY is used to integrate the menus and avatar placement. It should be as simple as importing vrcfury in VRC Creator Companian and dragging a prefab onto the base of the avatar and uploading. 

# Goals
## Long-Time Goals
 - More App support
 - Improved VRC Integration
 - Live Server Configuration
 - Better Error handling
 - Working UI
 - Automatic Unity Installer
 - Modular Structure
 - Custom/Easy Feedback Configurations

## Current Areas of Improvment:
My time for this project is very limited at the moment since I work 60-70hrs a week and have medical issues. ANY little thing helps, even if it is just reordering what is already there. Anyone willing to write good(readable) documentation for the project is worth their weight in gold to me.

There are ALOT of areas that need improvement immediately. The current codebase is a wreck, there is no proper scope management, and I kind of scattered functions willy-nilly during initial developement. 
 
### Urgent-ish needs:
   - [ ] Major Refactoring
      - [ ] split out functions to their own modules
      - [ ] implement proper scope management
      - [ ] document functions/objects
   -  [x] Start project docs 
      - [ ] The goal is to have an actual wiki eventuallys
   -  [x] Create Platform.io project
      - [ ] Same documentation standards as the server. 
   - [ ] Streamline Setup 
      - [ ] auto start with vrc
      - [ ] edit batch file to pull updates from github
      - [ ] edit batch file to check configurations


# Design Principles
Contribution is more than appreciated, but please keep it close/aligned with the projects over all goals:
 - Robust 
    - not many "hacky" work arounds
    - feel free to open a branch on your own fork if you would like to work in collaboration before merging to main
 - Simple To set up 
    - users shouldn't have to spend half an hour downloading python dependencies, something similar to AUTOMATIC's Stable Diffusion is the goal. 
 - Follow common Python syntax, such as snake case variables
 - **Readable Code** 
    - I would prefer having slightly less performant code if it is easily understandable. 
    - Please avoid ambigous variable naming (temp, i, j, etc.)

If the project takes off than rules and goals can change as needed. These are just my starting out thoughts.

