ac7paramnomore = 0xff
ac7parambeat = 0x01
ac7paramtempo = 0x02
ac7parammeasures = 0x06
ac7paramparts = 0x07
ac7paramtrackidx = 0x20
ac7parammixeridx = 0x21
ac7parampartidx = 0x22

ac7partname = {
    0: "Percussion",
    1: "Drums",
    2: "Bass",
    3: "Chord 1",
    4: "Chord 2",
    5: "Chord 3",
    6: "Chord 4",
    7: "Chord 5",
}

ac7partid = {
    "Percussion": 0,
    "Drums"     : 1,
    "Bass"      : 2,
    "Chord 1"   : 3,
    "Chord 2"   : 4,
    "Chord 3"   : 5,
    "Chord 4"   : 6,
    "Chord 5"   : 7,
    "major"     : 8,
    "minor"     : 0xa,
}

INTRO1 = 0
VAR1 = 1
VAR2 = 2
FILL1 = 3
FILL2 = 4
END1 = 5
INTRO2 = 6
VAR3 = 7
VAR4 = 8
FILL3 = 9
FILL4 = 10
END2 = 11

ac7elements = {INTRO1: "intro (1)", VAR1: "normal (var 1)", VAR2: "variation (var 2)", FILL1: "normal fill-in (1)", FILL2 "variation fill-in (2)", END1: "ending (1)",
               INTRO2: "intro (2)", VAR3: "variation 3", VAR4: "variation 4", FILL3: "fill-in (3)",  FILL4: "fill-in (4)", END2: "ending (2)" }