from collections import defaultdict


class Ac7CasioEventAnalyzer(object):
    def __init__(self):
        chromatic_scale = [['c', 'b#', 'dbb', 'd--'],  # one row contains all synonyms (i.e. synonym for our purpose)
                           ['c#', 'bx', 'db', 'd-'],
                           ['d', 'cx', 'ebb', 'e--'],
                           ['d#', 'eb', 'e-', 'fbb', 'f--'],
                           ['e', 'dx', 'fb', 'f-'],
                           ['f', 'e#', 'gbb', 'g--'],
                           ['f#', 'ex', 'gb', 'g-'],
                           ['g', 'fx', 'abb', 'a--'],
                           ['g#', 'ab', 'a-'],
                           ['a', 'gx', 'bbb', 'b--'],
                           ['a#', 'bb', 'b-', 'cbb', 'c--'],
                           ['b', 'ax', 'cb', 'c-']]

        corner_case_octave_lower = {"b#", "bx"}
        corner_case_octave_higher = {"cb", "c-", "cbb", "c--"}
        self.midi_to_note = defaultdict(lambda: [])
        notenum = 0
        for octave in range(11):
            for note_synonyms in chromatic_scale:
                if notenum <= 127:
                    for note in note_synonyms:
                        o = octave - 1
                        if note in corner_case_octave_lower:
                            o = o - 1
                        elif note in corner_case_octave_higher:
                            o = o + 1
                        self.midi_to_note[notenum].append("{0}{1}".format(note, o))
                    notenum += 1

    # note: highly speculative...
    def _annotate(self, casioevent):
        if casioevent['note_or_event'] < 127 and casioevent['vel_or_val'] != 0:
            casioevent['annotation'] = 'note {0} on with volume {1}'.format(
                self.midi_to_note[casioevent['note_or_event']][0], casioevent['vel_or_val'])
        if casioevent['note_or_event'] < 127 and casioevent['vel_or_val'] == 0:
            casioevent['annotation'] = 'note {0} off'.format(self.midi_to_note[casioevent['note_or_event']][0])
        if casioevent['note_or_event'] == 176 and casioevent['vel_or_val'] != 0:
            casioevent['annotation'] = 'mod wheel on (value {0})'.format(casioevent['vel_or_val'])
        if casioevent['note_or_event'] == 176 and casioevent['vel_or_val'] == 0:
            casioevent['annotation'] = 'mod wheel off'
        if casioevent['note_or_event'] == 229:
            casioevent['annotation'] = 'start of user recorded data'
        if casioevent['note_or_event'] == 255 and casioevent['vel_or_val'] != 0:
            casioevent['annotation'] = 'longdelta doesn\'t fit in single BYTE; longdelta = (vel_or_val << 8) + delta'
        if casioevent['note_or_event'] == 255 and casioevent['vel_or_val'] == 0 and casioevent['delta'] == 0:
            casioevent['annotation'] = 'pseudoevent to have even number?'
        if casioevent['note_or_event'] == 181:
            casioevent['annotation'] = 'modulation wheel'
        if casioevent['note_or_event'] == 186:
            casioevent['annotation'] = 'filter cut-off'
        if casioevent['note_or_event'] == 187:
            casioevent['annotation'] = 'filter resonance'
        if casioevent['note_or_event'] == 185:
            casioevent['annotation'] = 'pitch bend range'
        if casioevent['note_or_event'] == 142:
            casioevent['annotation'] = 'pitch bend value {0}'.format(casioevent['vel_or_val'])
        if casioevent['note_or_event'] == 252:
            casioevent['annotation'] = 'end of part; longdelta = (vel_or_val << 8) + delta'
        # speculative
        if casioevent['note_or_event'] == 135:
            casioevent['annotation'] = 'Expression LSB'
        if casioevent['note_or_event'] == 141:
            casioevent['annotation'] = 'after touch'
        if casioevent['note_or_event'] == 160:
            casioevent['annotation'] = "DANGER! Triggers SW failure. Don't use!"
        if casioevent['note_or_event'] == 169:
            casioevent['annotation'] = "Reset all parameters to default values"
        if casioevent['note_or_event'] == 177:
            casioevent['annotation'] = "Hold/sustain pedal"
        if casioevent['note_or_event'] == 178:
            casioevent['annotation'] = "Soft pedal"
        if casioevent['note_or_event'] == 179:
            casioevent['annotation'] = "Sostenuto pedal"
        if casioevent['note_or_event'] == 188:
            casioevent['annotation'] = "attack time"
        if casioevent['note_or_event'] == 189:
            casioevent['annotation'] = "release time"
        if casioevent['note_or_event'] == 224:
            casioevent['annotation'] = "chord conversion table 0-15"
        if casioevent['note_or_event'] == 225:
            casioevent['annotation'] = "chord inversion (0=off;1=on;2=7th;3=undocumented setting for forcing 7th"
        if casioevent['note_or_event'] == 226:
            casioevent['annotation'] = "retrigger (2=off; other=on)"
        if casioevent['note_or_event'] == 227:
            casioevent['annotation'] = "tempo increase (add value to original tempo in bpm, to max of 255"
        if casioevent['note_or_event'] == 228:
            casioevent['annotation'] = "tempo slowdown (subtract value from original tempo to minimum of 20"
        if casioevent['note_or_event'] == 230:
            casioevent['annotation'] = "highest note after chord conversion (0-127)"
        if casioevent['note_or_event'] == 231:
            casioevent['annotation'] = "UNKNOWN"
        if casioevent['note_or_event'] == 233:
            casioevent['annotation'] = "(Casio - specific MIDI CC 0x59)"
