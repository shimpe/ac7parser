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
        self.midi_to_note = defaultdict(lambda:[])
        notenum = 0
        for octave in range(10):
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
            casioevent['annotation'] = 'note {0} on with volume {1}'.format(self.midi_to_note[casioevent['note_or_event']][0], casioevent['vel_or_val'])
        if casioevent['note_or_event'] < 127 and casioevent['vel_or_val'] == 0:
            casioevent['annotation'] = 'note {0} off'.format(self.midi_to_note[casioevent['note_or_event']][0])
        if casioevent['note_or_event'] == 176 and casioevent['vel_or_val'] != 0:
            casioevent['annotation'] = 'mod wheel on'
        if casioevent['note_or_event'] == 176 and casioevent['vel_or_val'] == 0:
            casioevent['annotation'] = 'mod wheel off'
        if casioevent['note_or_event'] == 229:
            casioevent['annotation'] = 'recording data event? start of track? debugging event?'
        if casioevent['note_or_event'] == 227:
            casioevent['annotation'] = 'UNKNOWN'
        if casioevent['note_or_event'] == 228:
            casioevent['annotation'] = 'UNKNOWN'
        if casioevent['note_or_event'] == 255 and casioevent['vel_or_val'] != 0:
            casioevent['annotation'] = 'longdelta doesn\'t fit in single BYTE; value=longdelta/256; delta=longdelta & 0xff'
        if casioevent['note_or_event'] == 255 and casioevent['vel_or_val'] == 0 and casioevent['delta'] == 0:
            casioevent['annotation'] = 'pseudoevent to have even number?'
        if casioevent['note_or_event'] == 181:
            casioevent['annotation'] = 'expression'
        if casioevent['note_or_event'] == 186:
            casioevent['annotation'] = 'cut-off'
        if casioevent['note_or_event'] == 187:
            casioevent['annotation'] = 'harmonics'
        if casioevent['note_or_event'] == 185:
            casioevent['annotation'] = 'pitch bend range'
        if casioevent['note_or_event'] == 142:
            casioevent['annotation'] = 'pitch bend value {0}'.format(casioevent['vel_or_val'])
        if casioevent['note_or_event'] == 252:
            casioevent['annotation'] = 'end of part; value=longdelta/256; delta=longdelta & 0xff'
