class Ac7TrackLockRemover(object):
    def __init__(self):
        pass

    def remove_lock(self, casioeventlist):
        """speculative: remove event 228 and insert event 229 at begin of part"""
        filtered_event_list = [ev for ev in casioeventlist if ev['note_or_event'] != 228]
        first_event = filtered_event_list[0]
        if first_event['note_or_event'] != 229:
            original = filtered_event_list.copy()
            filtered_event_list = [{'delta': 0,
                                    'note_or_event': 229,
                                    'vel_or_val': 0}]
            filtered_event_list.extend(original)

        return filtered_event_list
