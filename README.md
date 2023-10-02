# What is this?
A script that modifies smd animation files to work with the proportion trick.
https://steamcommunity.com/sharedfiles/filedetails/?id=887935033 

It's usually more noticeable when the resulting custom model is smaller than the original models, but simply put a small character tends to bounce a lot and end up looking floaty or even worse just clipping through the ground or floating.

# How to use.
1. Multiply your animations by a value. Less than 1 makes any movements less noticeable. Higher than 1 makes them more pronounced.(note this only affects translations not rotations) 
2. Set Scale to 1.0 and start tweaking the Vertical Offset value with positive or negative values, while checking hlmv, until the character is grounded.

# Advanced Notes.
- The semicolon in the default_bones.txt specifies if the bone should be affected by the Vertical Offset.
- You should update the bone_indexes.txt to match the bones of your Original Player Model. You can get these from opening up an animation .smd from the Original Player model and copying the bone names from nodes to end.
(The formatting is whitespace sensitive so make sure it looks like the provided default_bones.txt)
