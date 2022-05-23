from .classes.parser import *

# TODO: figure out what to do with multiple ingredient strengths
class StrengthParser(Parser):
    parser_type = 'strength'
    match_keys = ['strength', 'strength_max', 'strength_unit', 'strength_text_start', 'strength_text_end', 'strength_text']
    def normalize_pattern(self):
        strength_patterns = []
        for n, p in STRENGTH_UNITS.items():
            # add the name of the pattern to the list of matched patterns
            p.append(n)
            # and join them with a | character
            # and add them to the strength_patterns array
            strength_patterns.append(r'|'.join(p))        
        pattern = re.compile(r'(?<!no more than)(?<!do not exceed)(?<!not to exceed)(?<!\bnmt)(?<!\bnte)\s*\(*\**(?P<strength>' + RE_RANGE + r')\**\)*(\s?\(.*\)\s?)?(?:\s*(?P<strength_unit>' + r'|'.join(strength_patterns) + r')\b)', flags = re.I)
        return pattern
    def normalize_match(self, match):
        # the standard RE_RANGE pattern will mach 1/2 which is fine for dose, but 5/325 is to complicated for strength, so disgard it for now
        if match.group('strength').find('/') < 0:
            strength_range = split_range(match.group('strength'))
            strength, strength_max = strength_range
            strength_unit = get_normalized(STRENGTH_UNITS, match.group('strength_unit'))
            strength_text_start, strength_text_end = match.span()
            strength_text = match[0]
        else:
            strength = strength_max = strength_unit = strength_text_start = strength_text_end = strength_text = None
        return self.generate_match({'strength': strength, 'strength_max': strength_max, 'strength_unit': strength_unit, 'strength_text_start': strength_text_start, 'strength_text_end': strength_text_end, 'strength_text': strength_text})

parsers = [
    StrengthParser()
]

#print(StrengthParser().parse('take one capsule (30 mg) prn nausea for 5 days'))