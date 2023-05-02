# Scid ECO
This script converts a modern openings database into a format that [scid](https://scidvspc.sourceforge.net) features. The motivation here is that Scid comes with an ECO database that hasn't been updated since 2014, and since then many new openings and novelties have been introduced. As Scid says on its [website](https://scidvspc.sourceforge.net/doc/ECO.htm): "The ECO system is however fairly limited, and insufficient for modern games".

## Usage
- Download Lichess's chess openings from [here](https://github.com/lichess-org/chess-openings) in this directory
- Run `python scid_eco.py`
- The file `openings.eco` should have been generated