from .classes.parser import *

class FrequencyParser(Parser):
	parser_type = 'frequency'
	match_keys = ['frequency', 'frequency_max', 'period', 'period_max', 'period_unit', 'time_duration', 'time_duration_unit', 'day_of_week', 'time_of_day', 'offset', 'bounds', 'count', 'frequency_text_start', 'frequency_text_end', 'frequency_text', 'frequency_readable']

# x1 | x 1
# exclude if followed by: day | week | month
# one time only
# count = 1
class FrequencyOneTime(FrequencyParser):
	pattern = r'(?:x\s*1\\b(?!day| day|d\b| d\b|week| week|w\b| w\b|month| month|mon|m\b| m\b| mon\b)|(?:1|one) time(?: only)?|for (?:1|one) dose|once$|once in imaging|at (?:the )?(?:first|1st) (?:onset:sign) of symptoms)'
	def normalize_match(self, match):
		count = 1
		frequency_text_start, frequency_text_end = match.span()
		frequency_text = match.group(0)
		frequency_readable = get_frequency_readable(count=count)
		# TODO: normalize text numbers to integer numbers - maybe make separate normalize_period_unit function that also hits the text_to_int function?
		return self.generate_match({'count': count, 'frequency_text_start': frequency_text_start, 'frequency_text_end': frequency_text_end, 'frequency_text': frequency_text, 'frequency_readable': frequency_readable})

# bid | tid | qid
# bid-tid, bid or tid
# TODO: account for bid-tid being min 2 and max 3 times per day - currently it only finds the max of 3
# frequency = a (2 if b, 3 if t, 4 if q), period = 1, periodUnit = d
class FrequencyXID(FrequencyParser):
	pattern = r'(?:\b(?:\s*(?:to|-|or)\s*)?(?P<frequency>b|t|q)\.?i\.?d\b\.?\b)+'
	def normalize_match(self, match):
		frequency_dict = { 'b': 2, 't': 3, 'q': 4 }
		frequency = frequency_dict.get(match.group('frequency').lower(), None)
		period = 1
		period_unit = 'day'
		frequency_text_start, frequency_text_end = match.span()
		frequency_text = match.group(0)
		frequency_readable = get_frequency_readable(frequency=frequency,period=period,period_unit=period_unit)
		return self.generate_match({'frequency': frequency, 'period': period, 'period_unit': period_unit, 'frequency_text_start': frequency_text_start, 'frequency_text_end': frequency_text_end, 'frequency_text': frequency_text, 'frequency_readable': frequency_readable})

# q | every | each
# 4 | 4-6 | 4 to 6 | four | four-six | four to six
# hours | days | weeks | months | h | hrs | hr | min | mins | mon
# (a: normalize 'to' to '-', and explode)
# NOTE: optional duplicate RE_RANGE accounts for sigs like every 12 (twelve) hours
# frequency = 1, period = a[0], periodUnit = b (normalize to h, d, wk, min), [periodMax = a[1]]
class FrequencyEveryXDay(FrequencyParser):
	pattern = r'(?:q|every|each)\s?(?P<period>' + RE_RANGE + r')(?:\s' + RE_RANGE + r'\s)?\s?(?P<period_unit>month|mon|hour|day|d\b|week|wks\b|wk\b|h\b|hrs\b|hr\b|min)'
	def normalize_match(self, match):
		frequency = 1
		period, period_max = split_range(match.group('period'))
		period_unit = get_normalized(PERIOD_UNIT, match.group('period_unit'))
		frequency_text_start, frequency_text_end = match.span()
		frequency_text = match.group(0)
		frequency_readable = get_frequency_readable(frequency=frequency,period=period,period_max=period_max,period_unit=period_unit)
		# TODO: normalize text numbers to integer numbers - maybe make separate normalize_period_unit function that also hits the text_to_int function?
		return self.generate_match({'frequency': frequency, 'period': period, 'period_max': period_max, 'period_unit': period_unit, 'frequency_text_start': frequency_text_start, 'frequency_text_end': frequency_text_end, 'frequency_text': frequency_text, 'frequency_readable': frequency_readable})

# 4 | four | 4-6 | 4 to 6 | 4 or 6 | four-six | four to six | four or six
# time(s) | x
# [per | a | each | /]
# day | daily | week | weekly | month | monthly
# 2-3 times daily
# (a: remove 'times' or 'x', normalize 'to' to '-', and explode)
# frequency = a[0], frequencyMax = a[1], period = 1, periodUnit = b (normalize to d, wk, mo, yr)
# frequency = a (1 if once, 2 if twice), period = 1, periodUnit = b (normalize to d, wk, mo, yr)
# NOTE: 'daily' won't match this pattern because it requires specific times *per* day
class FrequencyXTimesPerDay(FrequencyParser):
	pattern = r'(?P<frequency>' + RE_RANGE + r'\s*(?:time(?:s)?|x|nights|days)|once|twice)\s*(?:per|a|each|every|\/)\s*(?P<period_unit>day|week|month|year|d\b|w\b|mon|m\b|yr\b)'
	def normalize_match(self, match):
		frequency = frequency_max = match.group('frequency')
		if (frequency):
			frequency, frequency_max = split_frequency_range(frequency)
		else:
			frequency = 1
		period = 1
		period_unit = get_normalized(PERIOD_UNIT, match.group('period_unit'))
		frequency_text_start, frequency_text_end = match.span()
		frequency_text = match.group(0)
		frequency_readable = get_frequency_readable(frequency=frequency,frequency_max=frequency_max,period=period,period_unit=period_unit)
		# TODO: normalize text numbers to integer numbers - maybe make separate normalize_period_unit function that also hits the text_to_int function?
		return self.generate_match({'frequency': frequency, 'frequency_max': frequency_max, 'period': period, 'period_unit': period_unit, 'frequency_text_start': frequency_text_start, 'frequency_text_end': frequency_text_end, 'frequency_text': frequency_text, 'frequency_readable': frequency_readable})

# every | each | per | q
# [other]
# day | week | month | morning | afternoon | evening | night | hs
# TODO: combine with the qpm/qhs/qday/qdaily group above (not sure if this still applies)
# frequency = 1, period = 1 (or 2 if a is not null), periodUnit = b (normalize to d, wk, mo), [when = b (normalize to MORN, AFT, EVE, etc]
class FrequencyEveryDay(FrequencyParser):
	pattern = r'(?:every|each|q|per)\s*(?P<period>other\b|o\b)?\s*(?:day (?:in the|at)\s*)?(?P<period_unit>hour|day|week|month|morning|afternoon|evening at bedtime|bedtime|evening|night|hs\b|pm\b|am\b|d\b)'
	def normalize_match(self, match):
		frequency = 1
		period = 2 if match.group('period') else 1
		period_unit = get_normalized(PERIOD_UNIT, match.group('period_unit'))
		frequency_text_start, frequency_text_end = match.span()
		frequency_text = match.group(0)
		frequency_readable = get_frequency_readable(frequency=frequency,period=period,period_unit=period_unit)
		return self.generate_match({'frequency': frequency, 'period': period, 'period_unit': period_unit, 'frequency_text_start': frequency_text_start, 'frequency_text_end': frequency_text_end, 'frequency_text': frequency_text, 'frequency_readable': frequency_readable})

# every | on
# Thursday
# Monday, Tuesday, Wednesday, and Friday
# dayOfWeek = a
class FrequencySpecificDayOfWeek(FrequencyParser):
	pattern = r'(?:every|on|q)\s+(?P<day_of_week>(?:(?:\s*(?:and|&|\+|,)\s*)*(?:' + RE_DAYS_OF_WEEK + '))+)'
	def normalize_match(self, match):
		# TODO: normalize days of week to be comma or pipe delimited - tuesday and thursday -> tuesday|thursday or tuesday,thursday
		day_of_week = match.group('day_of_week')
		frequency_text_start, frequency_text_end = match.span()
		frequency_text = match.group(0)
		frequency_readable = get_frequency_readable(day_of_week=day_of_week)
		# TODO: normalize text numbers to integer numbers - maybe make separate normalize_period_unit function that also hits the text_to_int function?
		return self.generate_match({'day_of_week': day_of_week, 'frequency_text_start': frequency_text_start, 'frequency_text_end': frequency_text_end, 'frequency_text': frequency_text, 'frequency_readable': frequency_readable})


# once | twice | 3-4 times
# daily | nightly | weekly | monthly | yearly
# NOTE: this is where 'daily' matches
# once daily, twice monthly, daily
# (a: remove 'times' or 'x')
# frequency = a[0], frequencyMax = a[1], period = 1, periodUnit = b (normalize to d, wk, mo, yr)
# frequency = a (1 if once, 2 if twice, 1 if null), period = 1, periodUnit = b (normalize to d, wk, mo, yr)
class FrequencyXTimesDaily(FrequencyParser):
	pattern = r'(?:(?P<frequency>' + RE_RANGE + r'\s*(?:time(?:s)?|x)|once|twice)(?: \ba\b| per)?\s?)?(?P<period_unit>day\b|\bd\b|daily|dialy|weekly|monthly|yearly|\bhs\b)'
	def normalize_match(self, match):
		frequency = frequency_max = match.group('frequency')
		if (frequency):
			frequency, frequency_max = split_frequency_range(frequency)
		else:
			frequency = 1
		period = 1
		period_unit = get_normalized(PERIOD_UNIT, match.group('period_unit'))
		frequency_text_start, frequency_text_end = match.span()
		frequency_text = match.group(0)
		frequency_readable = get_frequency_readable(frequency=frequency,frequency_max=frequency_max,period=period,period_unit=period_unit)
		# TODO: normalize text numbers to integer numbers - maybe make separate normalize_period_unit function that also hits the text_to_int function?
		return self.generate_match({'frequency': frequency, 'frequency_max': frequency_max, 'period': period, 'period_unit': period_unit, 'frequency_text_start': frequency_text_start, 'frequency_text_end': frequency_text_end, 'frequency_text': frequency_text, 'frequency_readable': frequency_readable})


# in the
# morning | evening | afternoon
# frequency = 1, when = a
class FrequencyInTheX(FrequencyParser):
	pattern = r'in the\s*(morning|evening|afternoon)'
	def normalize_match(self, match):
		frequency = 1
		period = 1
		period_unit = 'day'
		frequency_text_start, frequency_text_end = match.span()
		frequency_text = match.group(0)
		frequency_readable = get_frequency_readable(frequency=frequency,period=period,period_unit=period_unit)
		return self.generate_match({'frequency': frequency, 'period': period, 'period_unit': period_unit, 'frequency_text_start': frequency_text_start, 'frequency_text_end': frequency_text_end, 'frequency_text': frequency_text, 'frequency_readable': frequency_readable})


# at
# bedtime | night | nightly
# frequency = 1, when = a (normalize to HS)
class FrequencyAtBedtime(FrequencyParser):
	pattern = r'((?:at )?bedtime|(?:at )night|nightly)'
	def normalize_match(self, match):
		frequency = 1
		period = 1
		period_unit = 'day'
		frequency_text_start, frequency_text_end = match.span()
		frequency_text = match.group(0)
		frequency_readable = get_frequency_readable(frequency=frequency,period=period,period_unit=period_unit)
		return self.generate_match({'frequency': frequency, 'period': period, 'period_unit': period_unit, 'frequency_text_start': frequency_text_start, 'frequency_text_end': frequency_text_end, 'frequency_text': frequency_text, 'frequency_readable': frequency_readable})


class FrequencyAsDirected(FrequencyParser):
	pattern = r'as directed(?: on package)?|ad lib|as instructed|see admin instructions|see notes'
	def normalize_match(self, match):
		# TODO: how to capture just text?
		# text = 'as directed'
		frequency_text_start, frequency_text_end = match.span()
		frequency_text = match.group(0)
		frequency_readable = frequency_text
		# TODO: normalize text numbers to integer numbers - maybe make separate normalize_period_unit function that also hits the text_to_int function?
		return self.generate_match({'frequency_text_start': frequency_text_start, 'frequency_text_end': frequency_text_end, 'frequency_text': frequency_text, 'frequency_readable': frequency_readable})

"""
TODO: improvements:
What about "at 8am" timings of meds?
Maybe check for "with meals" and infer three times daily?
"""

parsers = [
	FrequencyOneTime(),
	FrequencyXID(),
	FrequencyEveryXDay(),
	FrequencyXTimesPerDay(),
	FrequencyEveryDay(),
	FrequencySpecificDayOfWeek(),
	FrequencyXTimesDaily(),
	FrequencyInTheX(),
	FrequencyAtBedtime(),
	FrequencyAsDirected(),
]