This is a prefab designed to work with this project:
https://github.com/virtuallyaverage/VRC-Haptics-Host

NOTE: There are two versions, one pre-sized for female proportions and one for male.
 - Designated _fem and _masc

TO USE:
 -> Open a vrc creator companion project with an avatar that you want to apply haptics to.
 -> Add VRCFURY to the creator project if not already.
 -> Import haptics.unitypackage
 -> Place PC prefab on avatar root. (Usually right next to the Armature) 
   - A visualizer only version is included, for quest. The 16 collider limit on VRC prevents native quest utilization though.
   - NOTE: Quest users can interact and trigger the haptics, but the vest WILL NOT connect to the quest itself.
 -> Scale and move avatar nodes to your liking. (usually you want to get as close to your IRL Mounting as possible)
   - MAKE SURE to move the whole numbered colider node. If you just move the visualizer the collider will still be in the same place.