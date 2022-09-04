from .classes.parser import *

# in the
# morning | evening | afternoon
# NOTE: nightly is weird, but matches here too
class WhenParser(Parser):
	parser_type = 'when'
	match_keys = ['when', 'when_text_start', 'when_text_end', 'when_text', 'when_readable']
	pattern = r'(?P<when_relation>with|\bc\.|\bc|before|\ba|\ba\.|after|\bp|\bp\.|in the|at|every|each|\bq|\bq.|night)(?: each| every)?(?P<when_time>\s?(?:c\b|c\.\b|meal(?:s)? and at bedtime|meal(?:s)?|c\.m\.\b|cm\b|breakfast|c\.d\.\b|cd\b|lunch|c\.v\.\b|cv\b|dinner|morning before breakfast|morning|morn|a\.m\.\b|am\b|evening at bedtime|bedtime|evening|eve|aft(?:ernoon)?|p\.m\.\b|pm\b|night at bedtime|night|hs\b|h\.s\.\b|ly))'
	def normalize_match(self, match):
		# TODO: normalize before to 'a' and after to 'p', etc
		# TODO: normalize meals to 'm', etc
		when_relation = match.group('when_relation')
		when_time = match.group('when_time')
		when = get_normalized(WHEN, when_relation + when_time)
		when_text_start, when_text_end = match.span()
		when_text = match.group(0)
		when_readable = self.get_readable(when=when)
		return self.generate_match({'when': when, 'when_text_start': when_text_start, 'when_text_end': when_text_end, 'when_text': when_text, 'when_readable': when_readable})
	def get_readable(self, when=None):
		readable = when if when else ''
		return readable

# Things that don't match the more common patterns above
class OtherWhenParser(WhenParser):
	pattern = r'(?P<when>bedtime|\bam\b|\bhs\b)'
	def normalize_match(self, match):
		when = match.group('when')
		when = get_normalized(WHEN, when)
		when_text_start, when_text_end = match.span()
		when_text = match.group(0)
		when_readable = self.get_readable(when=when)
		return self.generate_match({'when': when, 'when_text_start': when_text_start, 'when_text_end': when_text_end, 'when_text': when_text, 'when_readable': when_readable})


"""
PC	http://hl7.org/fhir/v3/TimingEvent	PC	after meal (from lat. post cibus)
PCM	http://hl7.org/fhir/v3/TimingEvent	PCM	after breakfast (from lat. post cibus matutinus)
PCD	http://hl7.org/fhir/v3/TimingEvent	PCD	after lunch (from lat. post cibus diurnus)
PCV	http://hl7.org/fhir/v3/TimingEvent	PCV	after dinner (from lat. post cibus vespertinus)
"""

parsers = [
	WhenParser(),
	OtherWhenParser(),
]