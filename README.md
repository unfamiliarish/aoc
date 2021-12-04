# Advent of Code
This is my needlessly complicated scaffolding for advent of code. 

I know most folks do quick and dirty scripting for AoC, but I guess I insisted on making a package with importable modules and functions. I'm happy with this approach, and that's all that matters :) 

## How to run 
Add the root-level `aoc/` folder to your `PYTHONPATH` env var, I did this in my `~/.bash_profile` with:
```
export PYTHONPATH=$PYTHONPATH:/path/to/aoc
```

In the root-level `aoc/` folder, run:
```
python aoc [day number]
```
where `day number` is replaced with 1-25, depending on which day of the advent calendar you want to execute. 

For example, the following runs the code for day 3:
```
python aoc 3
```
