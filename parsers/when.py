from .classes.parser import *

# in the
# morning | evening | afternoon
# NOTE: nightly is weird, but matches here too
class WhenParser(Parser):
	parser_type = 'when'
	match_keys = ['when', 'when_text_start', 'when_text_end', 'when_text']
	pattern = r'(?P<when_relation>with|\bc\.|\bc|before|\ba|\ba\.|after|\bp|\bp\.|in the|at|every|\bq|\bq.|night)(?: each| every)?(?P<when_time>\s?(?:c\b|c\.\b|meal(?:s)? and at bedtime|meal(?:s)?|c\.m\.\b|cm\b|breakfast|c\.d\.\b|cd\b|lunch|c\.v\.\b|cv\b|dinner|morning|morn|\ba\.m\.\b|\bam\b|evening at bedtime|bedtime|evening|eve|aft(?:ernoon)?|\bp\.m\.\b|\bpm\b|night|hs\b|h\.s\.\b|ly))'
	def normalize_match(self, match):
		# TODO: normalize before to 'a' and after to 'p', etc
		# TODO: normalize meals to 'm', etc
		when_relation = match.group('when_relation')
		when_time = match.group('when_time')
		when = get_normalized(WHEN, when_relation + when_time)
		when_text_start, when_text_end = match.span()
		when_text = match.group(0)
		return self.generate_match({'when': when, 'when_text_start': when_text_start, 'when_text_end': when_text_end, 'when_text': when_text})

"""
PC	http://hl7.org/fhir/v3/TimingEvent	PC	after meal (from lat. post cibus)
PCM	http://hl7.org/fhir/v3/TimingEvent	PCM	after breakfast (from lat. post cibus matutinus)
PCD	http://hl7.org/fhir/v3/TimingEvent	PCD	after lunch (from lat. post cibus diurnus)
PCV	http://hl7.org/fhir/v3/TimingEvent	PCV	after dinner (from lat. post cibus vespertinus)
"""

parsers = [
	WhenParser()
]