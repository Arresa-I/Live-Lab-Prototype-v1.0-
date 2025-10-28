import os
import sys
import json
from pathlib import Path
from typing import Set

# -------------------CORE CATEGORIES-------------------

# Skill = ["Agility", "Independence", "Endurance", "Sensitivity", "Timing", "Improvisation/Creativity"]
# Musical Dimensions = ["Rhythm & Breaks", "Harmony & Melody", "Structure"]
# Musical SubDimensions = ["Time Signature", "Musical Figure", "Groups/Duo", "Scales", "Chords", "Chord Progression", "Sections", "Shapes"]
# Techniques = ["Articulations", "Fills & Rolls", "Polyrhythm", "Rudiments", "Swing", "Arpeggio", "Ornaments", "Tremolo & Vibrato", "Syncopation"]
# Modes = ["Free", "Linear", "Layered", "Cue Point Drumming", "One Handed Drumming", "Layout"]

categories = {
    "Skill": ["Agility", "Independence", "Endurance", "Sensitivity", "Timing", "Improvisation/Creativity"],
    "Musical Dimensions": ["Rhythm", "Harmony", "Structure"],
    "Musical SubDimensions": ["Time Signatures", "Musical Figures", "Tuplets", "Scales", "Chords", "Chord Progressions", "Sections", "Forms"],
    "Techniques": ["Articulations", "Fills & Rolls", "Polyrhythm", "Rudiments", "Swing", "Arpeggios", "Ornaments", "Tremolo & Vibrato"],
    "Modes": ["Free", "Linear", "Layered", "Cue Point Drumming", "One Handed Drumming", "Layout"]
}

# Improved structure with nested details
improved_categories = {
    "Skill": { 
        "Agility": None,
        "Precision": None,
        "Independence": ["Hands", "Fingers"],
        "Endurance": None,
        "Sensitivity": None,
        "Improvisation/Creativity": None,
        "Focus": None,
        "Auditory": ["Pitch Detection", "Rhythm Sense", "Harmonic Progression Identification"],
        "Cognitive": ["Reading", "Memory", "Analysis"]
    },
    "Elements": { 
        "Rhythm": ["Time Signature", "Musical Figure", "Groups/Duo"],
        "Harmony & Melody": {
            "Scales": ["Major", "Natural Minor", "Harmonic Minor", "Ascending Melodic Minor", "Major Pentatonic", "Minor Pentatonic", "Blues"],
            "Modes": ["Ionian", "Dorian", "Phrygian", "Lydian", "Mixolydian", "Aeolian", "Locrian"],
            "Chords": ["Major", "Minor", "Diminished", "Augmented", "Major Seventh", "Minor Seventh", "Diminished Seventh", "Augmented Seventh", 
                       "Major Seventh", "Minor Seventh", "Suspended", "Power Chords", "Ninth Chords", "Eleventh Chords", "Thirteenth Chords"],
            "Chord Progression": None
        },
        "Structure": ["Sections", "Shapes", "Development"],
    },
    "Techniques": {
        "Articulations": ["Staccato", "Legato", "Portato", 
                          ("Tremolo", ["Fast Tremolo", "Slow Tremolo"])],
        "Fills & Rolls": ["Simple Fill", "Complex Fill",
                          ("Double Kick Roll", ["Fast Roll", "Slow Roll"])],
        "Polyrhythm": ["3 over 2", "4 over 3", "5 over 4"],
        "Rudiments": ["Paradiddle", "Flam", "Drag",
                      ("Two-hand Rudiments", ["Double Paradiddle", "Triple Paradiddle"])],
        "Swing": ["Classic Swing", "Modern Swing"],
        "Arpeggios": ["Major Arpeggio", "Minor Arpeggio", "Diminished Arpeggio"],
        "Ornaments": ["Trills", "Mordents", "Appoggiatura"],
        "Tremolo & Vibrato": ["String Tremolo", "String Vibrato",
                              ("Percussion Tremolo", ["Stick Tremolo", "Mallet Tremolo"])]
    },
    "Modes": ["1 Hand", "2 Hands", "Free", "Linear", "Layered", "Cue Point Drumming", "One Handed Drumming", "Layout"]
}

# Main dictionary that stores all the lists
# Add or remove categories here, as this is the main matrix on which the others depend
matched_lists = {
    "Skill": [],
    "Musical Dimensions": [],
    "Musical SubDimensions": [],
    "Techniques": [],
    "Modes": [],
    "Warmup": [],
    "Fundamentals": [],
    "Development": [],
    "Improvisation": [],
    "Goals": []
}

# -------------------RELATIONSHIPS-------------------

a = True
b = False

# NOTE: These can be reduced to matrices of a and b without using the "if" system

# Description of Matrices:
###    | m1 | m2 | m3 | 
###    |----|----|----|
### i1 |    |    |    |
###    |----|----|----|
### i2 |    |    |    |
###    |----|----|----|
### i3 |    |    |    |
###    |----|----|----|

# Skill-to-Skill Relationships

S2S_Mat = [[a,a,a,a,a,a],
          [a,a,a,a,a,a],
          [a,a,a,a,a,a],
          [a,a,a,a,a,a],
          [a,a,a,a,a,a],
          [a,a,a,a,a,a]]

S2S_Rel = {
    "Agility": {
        "Agility": True,
        "Independence": True,
        "Stamina": True,
        "Sensitivity": True,
        "Timing": True,
        "Improvisation/Creativity": True,
    },
    "Independence": {
        "Independence": True,
        "Stamina": True,
        "Sensitivity": True,
        "Timing": True,
        "Improvisation/Creativity": True,
    },
    "Endurance": {
        "Endurance": True,
        "Sensitivity": True,
        "Timing": True,
        "Improvisation/Creativity": True,
    },
    "Sensitivity": {
        "Sensitivity": True,
        "Timing": True,
        "Improvisation/Creativity": True,
    },
    "Timing": {
        "Timing": True,
        "Improvisation/Creativity": True,
    },
    "Improvisation/Creativity": {
        "Improvisation/Creativity": True,
    }
}

S2S_Rel2 = [["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""],["","","","","",""]]

S2S_Rel2[0][1] = "Enables each hand/finger to work independently."
S2S_Rel2[0][2] = "Play fast and complex patterns consistently."
S2S_Rel2[0][3] = "Finger agility enhances sensitivity when striking keys."
S2S_Rel2[0][4] = "Speed and agility contribute to better timing."
S2S_Rel2[0][5] = "Improvising fast and complex patterns."

S2S_Rel2[1][2] = "Maintain independence of hands/fingers over time."
S2S_Rel2[1][3] = "Control intensity and form in each hand/finger independently."
S2S_Rel2[1][4] = "Play different timings with each hand/finger."
S2S_Rel2[1][5] = "Improvise independently with each hand."

S2S_Rel2[2][3] = "Maintain intensity and shape over time."
S2S_Rel2[2][4] = "Maintain proper timing for extended periods."
S2S_Rel2[2][5] = "Improvise for long periods while keeping coherence."

S2S_Rel2[3][4] = "Play with intensity and shape at the right time."
S2S_Rel2[3][5] = "Improvise with dynamic intensity for nuance."

S2S_Rel2[4][5] = "Maintain timing while playing without references."

# Skill-to-Musical Dimension Relationships

S2MD_Mat = [[a,a,a],
           [a,a,a],
           [a,a,a],
           [a,a,b],
           [a,b,b],
           [a,a,a]]

S2MD_Rel = {
    "Agility": {
        "Rhythm & Breaks": True,
        "Harmony & Melody": True,
        "Structure": True,
    },
    "Independence": {
        "Rhythm & Breaks": True,
        "Harmony & Melody": True,
        "Structure": True,
    },
    "Stamina": {
        "Rhythm & Breaks": True,
        "Harmony & Melody": True,
        "Structure": True,
    },
    "Sensitivity": {
        "Rhythm & Breaks": True,
        "Harmony & Melody": True,
        "Structure": False,
    },
    "Timing": {
        "Rhythm & Breaks": True,
        "Harmony & Melody": False,
        "Structure": False,
    },
    "Improvisation/Creativity": {
        "Rhythm & Breaks": True,
        "Harmony & Melody": True,
        "Structure": True,
    },
}

S2MD_Rel2 = [["","",""],["","",""],["","",""],["","",""],["","",""],["","",""]]

S2MD_Rel2[0][0] = "Play fast rhythmic patterns or at high BPMs."
S2MD_Rel2[0][1] = "Play the right notes in complex patterns."
S2MD_Rel2[0][2] = "Play complex transitions and changes between parts."

S2MD_Rel2[1][0] = "Play different rhythms with each hand and finger."
S2MD_Rel2[1][1] = "Play different harmonic lines with each hand."
S2MD_Rel2[1][2] = "Play fills and rolls independently with each hand."

S2MD_Rel2[2][0] = "Play rhythmic patterns for long durations."
S2MD_Rel2[2][1] = "Play harmonic sequences for long durations."
S2MD_Rel2[2][2] = "Play entire pieces without fatigue."

S2MD_Rel2[3][0] = "Play rhythmic patterns, riffs, basslines, or melodies with desired intensity and shape."
S2MD_Rel2[3][1] = "Control harmonic dynamics as desired."

S2MD_Rel2[4][0] = "Play patterns, riffs, basslines, and melodies at the desired time."

S2MD_Rel2[5][0] = "Improvise various rhythmic, riff, and bassline patterns."
S2MD_Rel2[5][1] = "Improvise chord progressions, arpeggios, and melodies."
S2MD_Rel2[5][2] = "Improvise structural changes and entire compositions."


## Skill-Musical SubDimensions

### i = 0: Agility, 1: Independence, 2: Endurance, 3: Sensitivity, 4: Timing, 5: Improvisation
### m = 0: "Time Signature", "Musical Figures", "Tuplets", "Scales", "Chords", "Chord Progressions", "Sections", "Forms"

S2MSD_Mat = [[a,a,a,a,a,a,a,a],
             [a,a,a,a,a,a,a,a],
             [a,a,a,a,a,a,a,a],
             [a,a,a,a,a,a,b,b],
             [a,a,a,b,b,b,b,b],
             [a,a,a,a,a,a,a,b]]


## Skill-Technique

### i = 0: Agility, 1: Independence, 2: Endurance, 3: Sensitivity, 4: Timing
### m = 0: Articulations,
### 1: Fills & Rolls, 2: Polyrhythm, 3: Rudiments, 4: Swing
### 5: Arpeggios, 6: Ornaments, 7: Tremolo and Vibrato

S2T_Mat = [[b,a,b,a,b,a,a,b],
           [b,a,a,a,a,a,a,b],
           [b,a,a,a,a,b,b,b],
           [a,a,a,a,b,a,a,a],
           [b,a,a,a,a,a,a,b],
           [a,a,a,a,a,a,a,a]]


## Skill-Mode

### i = 0: Agility, 1: Independence, 2: Endurance, 3: Sensitivity, 4: Timing, 5: Improvisation
### m = 0: Free, 1: Linear, 2: Layered, 3: Cue Point Drumming, 4: One-Handed Drumming, 5: Layout

S2M_Mat = [[b,b,b,b,b,b],
           [b,a,b,b,a,b],
           [b,b,b,b,b,b],
           [b,b,b,b,b,b],
           [b,b,b,b,b,b],
           [a,a,a,a,a,a]]


## Musical Dimensions-SubDimensions

### i = 0: "Rhythm", "Harmony", "Structure"
### m = 0: "Time Signature", "Musical Figure", "Tuples", "Scales", "Chords", "Chord Progressións", "Sections", "Forms"

MD2MSD_Mat = [[a,a,a,b,b,b,b,b],
              [b,b,b,a,a,a,b,b],
              [b,b,b,b,b,b,a,a]]


## Musical Dimensions-Technique

### i = 0: Rhythm, 1: Harmony, 2: Structure
### m = 0: Articulations
###     1: Fills & Rolls, 2: Polyrhythm, 3: Rudiments, 4: Swing
###     5: Arpeggios, 6: Ornaments, 7: Tremolo and Vibrato

MD2T_Mat = [[b,a,a,a,a,b,b,b],
            [a,b,b,b,b,a,a,a],
            [b,a,b,b,b,b,b,b]]


## Musical Dimensions-Mode

### i = 0: Rhythm, 1: Harmony, 2: Structure
### m = 0: Freeform, 1: Linear, 2: Layered, 3: Cue Point, 4: One-Handed Drumming, 5: Layout

MD2M_Mat = [[b,b,b,b,a,a],
            [b,b,b,b,a,b],
            [b,b,b,b,b,b]]


## Musical SubDimensions-Techniques

### i = 0: "Time Signature", "Musical Figure", "Tuplets", "Scales", "Chords", "Chord Progressions", "Sections", "Forms"
### m = 0: Articulations,
###     1: Fills & Rolls, 2: Polyrhythm, 3: Rudiments, 4: Swing
###     5: Arpeggios, 6: Ornaments, 7: Tremolo and Vibrato

MSD2T_Mat = [[b,a,a,a,a,b,b,b],
             [b,a,a,a,a,b,b,b],
             [b,a,a,a,a,b,b,b],
             [a,b,b,b,b,a,a,a],
             [a,b,b,b,b,a,a,a],
             [a,b,b,b,b,a,a,a],
             [b,a,b,b,b,b,b,b],
             [b,b,b,b,b,b,b,b]]


## Musical SubDimensions-Modes

### i = 0: "Time Signature", "Musical Figure", "Tuplets", "Scales", "Chords", "Chord Progressions", "Sections", "Forms"
### m = 0: Free, 1: Linear, 2: Layered, 3: Cue Point, 4: One-Handed Drumming, 5: Layout

MSD2M_Mat = [[b,b,b,b,a,a],
             [b,b,b,b,a,a],
             [b,b,b,b,a,a],
             [b,b,b,b,a,b],
             [b,b,b,b,a,b],
             [b,b,b,b,a,b],
             [b,b,b,b,b,b],
             [b,b,b,b,b,b]]

# -------------------MATRIZ DE MATRICES-------------------

Relationship_Matrices = {
    cat1: {
        cat2: mat
        for cat2, mat in zip(categories, row)
    }
    for cat1, row in zip(categories, [
        [S2S_Mat, S2MD_Mat, S2MSD_Mat, S2T_Mat, S2M_Mat], 
        [S2MD_Mat, 0, MD2MSD_Mat, MD2T_Mat, MD2M_Mat],
        [S2MSD_Mat, MD2MSD_Mat, 0, MSD2T_Mat, MSD2M_Mat],
        [S2T_Mat, MD2T_Mat, MSD2T_Mat, 0, 0],
        [S2M_Mat, MD2M_Mat, MSD2M_Mat, 0, 0]
    ])
}


# -------------------INTERFACE-------------------

INTERFACES = ["All", "Keys", "Pads"]

# -------------------GENRES-------------------

all_tags: Set[str] = set()

# Folder where the script is located
folder_script = os.path.dirname(os.path.abspath(__file__))

# Path to a folder named 'Lessons' in the same folder
relative_path = os.path.join(folder_script, 'Lessons')

for root, _, files in os.walk(relative_path):
    for file_name in files:
        if file_name.endswith(".json"):
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "data" in data and isinstance(data["data"], dict):
                        tags = data["data"].get("genres")
                        if isinstance(tags, list):
                            for tag in tags:
                                if isinstance(tag, str):
                                    all_tags.add(tag.strip())
            except (json.JSONDecodeError, UnicodeDecodeError, OSError):
                continue

GENRES = sorted(all_tags)

# -------------------VARIABLES-------------------

# Cumulative list of selected items
listboxes_selections = {}

# Dictionary that records lessons (as keys) along with matching selected items
lessons = {}

# Dictionary that records selected lessons
selected_lessons = {}
