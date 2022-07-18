from .classes.parser import *

class MaxDoseParser(Parser):
    parser_type = 'max_dose'
    match_keys = ['max_dose_numerator_value', 'max_dose_numerator_unit', 'max_dose_denominator_value', 'max_dose_denominator_unit', 'max_dose_text_start', 'max_dose_text_end', 'max_dose_text', 'max_dose_readable']
    def normalize_pattern(self):
        dose_patterns = []
        for n, p in DOSE_UNITS.items():
            # add the name of the pattern to the list of matched patterns
            p.append(n)
            # and join them with a | character
            # and add them to the dose_patterns array
            dose_patterns.append(r'|'.join(p))        
        pattern = re.compile(r'(?:max(?: dose)|do not take more than|no more than|nmt|do not exceed)\s?(?P<dose>' + RE_RANGE + r')\s?(?P<dose_unit>' + r'|'.join(dose_patterns) + r')?\s?(?:per|/|in(?: a)?)\s?(?P<period>' + RE_RANGE + r')?\s?(?P<period_unit>day|hours|hour|hrs|hr|\bh\b|week|month|year|d\b|w\b|mon|m\b|yr)', flags = re.I)
        return pattern
    def normalize_match(self, match):
        dose_range = split_range(match.group('dose'))
        max_dose_numerator_value = dose_range[1] or dose_range[0]
        max_dose_numerator_unit = get_normalized(DOSE_UNITS, match.group('dose_unit')) if match.group('dose_unit') else None
        max_dose_denominator_value = None
        if match.group('period'):
            period_range = split_range(match.group('period')) 
            max_dose_denominator_value = period_range[1] or period_range[0]
        max_dose_denominator_unit = get_normalized(PERIOD_UNIT, match.group('period_unit')) if match.group('period_unit') else None
        max_dose_text_start, max_dose_text_end = match.span()
        max_dose_text = match[0]
        max_dose_readable = self.get_readable(
            max_dose_numerator_value=max_dose_numerator_value, 
            max_dose_numerator_unit=max_dose_numerator_unit, 
            max_dose_denominator_value=max_dose_denominator_value,
            max_dose_denominator_unit=max_dose_denominator_unit)
        return self.generate_match({'max_dose_numerator_value': max_dose_numerator_value, 'max_dose_numerator_unit': max_dose_numerator_unit, 'max_dose_denominator_value': max_dose_denominator_value, 'max_dose_denominator_unit': max_dose_denominator_unit, 'max_dose_text_start': max_dose_text_start, 'max_dose_text_end': max_dose_text_end, 'max_dose_text': max_dose_text, 'max_dose_readable': max_dose_readable})
    def get_readable(self, max_dose_numerator_value=None, max_dose_numerator_unit=None, max_dose_denominator_value=None, max_dose_denominator_unit=None):
        readable = 'max dose'
        readable += ' ' + str(max_dose_numerator_value) if max_dose_numerator_value else ''
        plural_dose_unit = max_dose_numerator_value and max_dose_numerator_value > 1
        if max_dose_numerator_unit:
            if plural_dose_unit:
                max_dose_numerator_unit += 'e' if max_dose_numerator_unit[-1:] == 'h' else ''
                max_dose_numerator_unit += 's' if max_dose_numerator_unit not in ['oz','mL','L','cm'] else ''
            readable += ' ' + max_dose_numerator_unit

        readable += ' per' if max_dose_denominator_value or max_dose_denominator_unit else ''
        readable += ' ' + str(max_dose_denominator_value) if max_dose_denominator_value else ''
        plural_duration = max_dose_denominator_value and max_dose_denominator_value > 1
        if max_dose_denominator_unit:
            max_dose_denominator_unit += 's' if plural_duration else ''
        readable += ' ' + max_dose_denominator_unit
        return readable

parsers = [
    MaxDoseParser(),
]
