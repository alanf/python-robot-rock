''' chords.py
    Author: Rich Snider <mrsoviet@cs.washington.edu>
    '''


Majors = {"C": ("C", "E", "G"),
          "C#": ("C#", "F", "G#"),
          "Db": ("Db", "F", "Ab"),  #repeat
          "D": ("D", "F#", "A"),
          "D#": ("D#", "G", "A#"),
          "Eb": ("Eb", "G", "Bb"),  #repeat
          "E": ("E", "G#", "B"),
          "E#": ("F", "A", "C"),
          "Fb": ("E", "G#", "B"),
          "F": ("F", "A", "C"),
          "F#": ("F#", "A#", "C#"),
          "Gb": ("Gb", "Bb", "Db"), #repeat
          "G": ("G", "B", "D"),
          "G#": ("G#", "C", "D#"),
          "Ab": ("Ab", "C", "Eb"),  #repeat
          "A": ("A", "C#", "E"),
          "A#": ("A#", "D", "F"),
          "Bb": ("Bb", "D", "F"),   #repeat
          "B": ("B", "D#", "F#"),
          "B#": ("C", "E", "G"),
          "Cb": ("B", "D#", "F#")}

Minors = {"C": ("C", "Eb", "G"),
          "C#": ("C#", "E", "G#"),
          "Db": ("Db", "E", "Ab"), #repeat
          "D": ("D", "F", "A"),
          "D#": ("D#", "F#", "A#"),
          "Eb": ("Eb", "Gb", "Bb"),#repeat
          "E": ("E", "G", "B"),
          "E#": ("F", "Ab", "C"),
          "Fb": ("E", "G", "B"),
          "F": ("F", "Ab", "C"),
          "F#": ("F#", "A", "C#"),
          "Gb": ("Gb", "A", "Db"), #repeat
          "G": ("G", "Bb", "D"),
          "G#": ("G#", "B", "D#"),
          "Ab": ("Ab", "B", "Eb"), #repeat
          "A": ("A", "C", "E"),
          "A#": ("A#", "C#", "F"),
          "Bb": ("Bb", "Db", "F"), #repeat
          "B": ("B", "D", "F#"),
          "B#": ("C", "Eb", "G"),
          "Cb": ("B", "D", "F#")}

Augmented = {"C": ("C", "E", "G#"),
             "C#": ("C#", "F", "Ab"),
             "Db": ("Db", "F", "A"),    #repeat?
             "D": ("D", "F#", "A#"),
             "D#": ("D#", "G", "Bb"),
             "Eb": ("Eb", "G", "B"),    #repeat?
             "E": ("E", "G#", "C"),
             "E#": ("F", "A", "C#"),
             "Fb": ("E", "G#", "C"),
             "F": ("F", "A", "C#"),
             "F#": ("F#", "A#", "Db"),
             "Gb": ("Gb", "Bb", "D"),   #repeat?
             "G": ("G", "B", "D#"),
             "G#": ("G#", "C", "Eb"),
             "Ab": ("Ab", "C", "E"),    #repeat?
             "A": ("A", "C#", "F"),
             "A#": ("A#", "D", "F"),
             "Bb": ("Bb", "D", "F#"),   #repeat?
             "B": ("B", "D#", "G"),
             "B#": ("C", "E", "G#"),
             "Cb": ("B", "D#", "G")}

Diminished = {"C": ("C", "Eb", "Gb"),
              "C#": ("C#", "E", "G"),
              "Db": ("Db", "E", "G"),    #repeat
              "D": ("D", "F", "Ab"),
              "D#": ("D#", "F#", "A"),
              "Eb": ("Eb", "Gb", "A"),   #repeat
              "E": ("E", "G", "Bb"),
              "E#": ("F", "Ab", "B"),
              "Fb": ("E", "G", "Bb"),
              "F": ("F", "Ab", "B"),
              "F#": ("F#", "A", "C"),
              "Gb": ("Gb", "A", "C"),    #repeat
              "G": ("G", "Bb", "Db"),
              "G#": ("G#", "B", "D"),
              "Ab": ("Ab", "B", "D"),    #repeat
              "A": ("A", "C", "Eb"),
              "A#": ("A#", "C#", "E"),
              "Bb": ("Bb", "Db", "E"),   #repeat
              "B": ("B", "D", "F"),
              "B#": ("C", "Eb", "Gb"),
              "Cb": ("B", "D", "F")}

Progressions = {"C": ("C", "F", "G"),
                "C#": ("C#", "F#", "G#"),
                "Db": ("Db", "Gb", "Ab"), #repeat
                "D": ("D", "G", "A"),
                "D#": ("D#", "G#", "A#"),
                "Eb": ("Eb", "Ab", "Bb"),  #repeat
                "E": ("E", "A", "B"),
                "E#": ("F", "Bb", "C"),
                "Fb": ("E", "A", "B"),
                "F": ("F", "Bb", "C"),
                "F#": ("F#", "B", "C#"),
                "Gb": ("Gb", "B", "Db"), #repeat
                "G": ("G", "C", "D"),
                "G#": ("G#", "C#", "D#"),
                "Ab": ("Ab", "Db", "Eb"),  #repeat
                "A": ("A", "D", "E"),
                "A#": ("A#", "D#", "F"),
                "Bb": ("Bb", "Eb", "F"),   #repeat
                "B": ("B", "E", "F#"),
                "B#": ("C", "F", "G"),
                "Cb": ("B", "E", "F#")}
          
