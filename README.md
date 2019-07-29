# dfletcher/factorio

Just playing around with Factorio recipes.

## Installation

`pip install -r Requirements.txt`

## Usage

### factorio-recipe-parser.lua

The file `factorio-recipe-parser.lua` comes from this Reddit thread https://www.reddit.com/r/factorio/comments/25iz4i/is_there_a_partsrecipe_list/ credit goes to u/pf_moore for the orignal version (updated for current Factorio data format) This script creates the file `ingredients.yml` which is checked into the repository, so if you are messing with these tools you only need to touch the Lua script if you want to change the formatm of ingredients.yml or fix problems with it. There is some work that could be done here... (1) some items have multiple types of factories that can make them (e.g solid-fuel-from-light-oil, solid-fuel-from-petroleum-gas, petroleum-gas
solid-fuel-from-heavy-oil all produce "solid-fuel" but currently the system sees them as different products. (2) The number of parts needed to construct things is not written in to the JSON nor used in the output currently.

This command will re-generate ingredients.yml:

`lua factorio-recipe-parser.lua > ingredients.yml`

### sort.py

Script `sort.py` generates `histogram.txt`, `non-ingredient-parts.yml`, and the `output/` directory with SVG graphs. The script currently takes no arguments.

The following command will regenerate all targets:

`python sort.py`

## Todo

1. Better representation of node (it's currently just a label with lines pointing at it).
1. Better positioning of nodes. Put terminals on the left and the final outputs pointing right.
1. Display number of parts needed next to each node input.
1. Highlight / bold the main target of the graph.
1. Enable users to make custom graphs specify inputs that already exist so do not need to be represented; and make graphs with multiple ouputs.
1. Display summary with termninals information, inputs and outputs for the graph.
