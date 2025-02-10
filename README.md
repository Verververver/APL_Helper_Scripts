# APL Helper Scripts

# Brief description of each tool
**Conditioner** - Adds the specified condition in the argument to each line.
**Line Trimmer** - Goes through line by line and removes that line and saves it as a permutation. This is to test each line's robustness.
**Shuffler** - Given the specific line index, goes through line by line and adds that specified action line in that position and saves it as a permutation. This is to test the positioning of each line.
**Splitter** - Goes through each line and splits the | (OR) condition.

# Instructions
1. Put your APL into "apl.simc" [(See example-input-and-apl-assumptions)](#example-input-and-apl-assumptions)
2. Edit argument parameters if needed
3. Run the relevant python script

# Example input and APL Assumptions
**Assumptions**

The code is designed so that it assumes the following:
 - No duplicate lines
 - Correct format and notations
 - The code is not designed to handle an entire APL paste (e.g., multile profiles of AOE and ST) but instead one profile at a time (e.g., single target APL)

**Example input should look like **
```
copy="Example"
talents=CAEAAAAAAAAAAAAAAAAAAAAAAYGbmtZBzwY2MYmZ0YMzYGzwwMYmZmZmZegZmZGzMzYmZZmmZWmFAAA0CAAAAAAGAAAAAAAAA

actions.standard_rotation=flamestrike,if=active_enemies>=variable.hot_streak_flamestrike&(buff.hot_streak.react|buff.hyperthermia.react)
actions.standard_rotation+=/pyroblast,if=buff.hot_streak.react|buff.hyperthermia.react
```
or see [apl.simc](https://github.com/Verververver/APL_Helper_Scripts/blob/main/apl.simc)



