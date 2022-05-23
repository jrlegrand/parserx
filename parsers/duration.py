from .classes.parser import *

class DurationParser(Parser):
    parser_type = 'duration'
    match_keys = ['duration', 'duration_max', 'duration_unit', 'duration_text_start', 'duration_text_end', 'duration_text']

# for x [more] days
class DurationParserForXDays(DurationParser):
    pattern = r'(?:for|x)\s*(?P<duration>' + RE_RANGE + r')\s*(?:more)?\s*(?P<duration_unit>year|month|week|day|yr\b|mon\b|wk\b|d\b)'
    def normalize_match(self, match):
        duration_range = split_range(match.group('duration'))
        duration_text_start, duration_text_end = match.span()
        # NOTE: PERIOD_UNIT has the same content that duration_unit needs for normalization
        duration_unit = get_normalized(PERIOD_UNIT, match.group('duration_unit'))
        duration, duration_max = duration_range
        duration_text = ' '.join(match.groups())
        return self.generate_match({'duration': duration, 'duration_max': duration_max, 'duration_unit': duration_unit, 'duration_text_start': duration_text_start, 'duration_text_end': duration_text_end, 'duration_text': duration_text})

# on day x
class DurationParserOnDayX(DurationParser):
    pattern = r'on day(?:s)?\s*(?P<duration>' + RE_RANGE + r')'
    def normalize_match(self, match):
        duration_range = split_range(match.group('duration'))
        duration_text_start, duration_text_end = match.span()
        duration = 1 if duration_range[0] == duration_range[1] or duration_range[1] == None else int(duration_range[1]) - int(duration_range[0]) + 1
        duration_unit = 'day'
        duration, duration_max = [duration, duration]
        duration_text = ' '.join(match.groups())
        return self.generate_match({'duration': duration, 'duration_max': duration_max, 'duration_unit': duration_unit, 'duration_text_start': duration_text_start, 'duration_text_end': duration_text_end, 'duration_text': duration_text})

parsers = [
    DurationParserForXDays(),
    DurationParserOnDayX()
]

#print(DurationParserForXDays().parse('take one prn nausea for 5 days'))