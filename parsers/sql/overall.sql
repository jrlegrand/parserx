select distinct sig.sig_text
, (case when sig.strength is not null and (sig.dose is null or (sig.dose is not null and sig.dose = 1)) then concat(sig.strength, if(sig.strength_max is not null, concat('-', sig.strength_max), ''))
    when sig.dose is not null then concat(sig.dose, if(sig.dose_max is not null, concat('-', sig.dose_max), ''))
    else null end) as parserx_vumc_dose
, dose_unit.destination_dose_unit_name as parserx_vumc_dose_unit
, route.destination_route_name as parserx_vumc_route
, (case when sig.frequency_max is null and sig.period_max is null then freq.destination_frequency_name
    else null end) as parserx_vumc_frequency
, vumc_sig.dose as vumc_dose
, vumc_sig.dose_unit as vumc_dose_unit
, vumc_sig.route as vumc_route
, vumc_sig.frequency_name as vumc_frequency

, (case when (
        (case when sig.strength is not null and (sig.dose is null or (sig.dose is not null and sig.dose = 1)) then concat(sig.strength, if(sig.strength_max is not null, concat('-', sig.strength_max), '')) when sig.dose is not null then concat(sig.dose, if(sig.dose_max is not null, concat('-', sig.dose_max), '')) else null end) = vumc_sig.dose 
        or
        ((case when sig.strength is not null and (sig.dose is null or (sig.dose is not null and sig.dose = 1)) then concat(sig.strength, if(sig.strength_max is not null, concat('-', sig.strength_max), '')) when sig.dose is not null then concat(sig.dose, if(sig.dose_max is not null, concat('-', sig.dose_max), '')) else null end) is null and vumc_sig.dose is null)
    )
    and (dose_unit.destination_dose_unit_name = vumc_sig.dose_unit or (dose_unit.destination_dose_unit_name is null and vumc_sig.dose_unit is null))
    and (route.destination_route_name = vumc_sig.route or (route.destination_route_name is null and vumc_sig.route is null))
    and (
        (case when sig.frequency_max is null and sig.period_max is null then freq.destination_frequency_name else null end) = vumc_sig.frequency_name
        or
        ((case when sig.frequency_max is null and sig.period_max is null then freq.destination_frequency_name else null end) is null and vumc_sig.frequency_name is null)
    )   
    then "Yes"
    else "No" end) as parserx_correct_yn

, sig.indication as parserx_vumc_indication
, vumc_sig.prn_reason_1 as vumc_indication
, (sig.period / sig.frequency) as ncit_frequency_value
, sig.period_unit as ncit_frequency_time_unit
, sig.*
, vumc_sig.*
from parserx.sig_sigparsed sig
left join vumc.sig_manually_parsed vumc_sig
    on sig.sig_text = lower(replace(vumc_sig.sig_text, '  ', ' '))
left join vumc.dose_unit dose_unit 
	on (case when sig.strength_unit is not null and (sig.dose_unit is null or (sig.dose_unit is not null and sig.dose = 1)) then sig.strength_unit
        when sig.dose_unit is not null then sig.dose_unit
        else null end) = dose_unit.dose_unit
left join vumc.route route
	on sig.route = route.route
left join vumc.frequency freq 
	on (sig.frequency = freq.frequency or (sig.frequency is null and freq.frequency is null))
	and (sig.frequency_max = freq.frequency_max or (sig.frequency_max is null and freq.frequency_max is null))
    and (sig.period = freq.period or (sig.period is null and freq.period is null))
    and (sig.period_max = freq.period_max or (sig.period_max is null and freq.period_max is null))
    and (sig.period_unit = freq.period_unit or (sig.period_unit is null and freq.period_unit is null))
    and (sig.time_duration = freq.time_duration or (sig.time_duration is null and freq.time_duration is null))
    and (sig.day_of_week = freq.day_of_week or (sig.day_of_week is null and freq.day_of_week is null))
    and (sig.time_of_day = freq.time_of_day or (sig.time_of_day is null and freq.time_of_day is null))
    and (sig.when = freq.when or (sig.when is null and freq.when is null))
    and (sig.offset = freq.offset or (sig.offset is null and freq.offset is null))
    and (sig.bounds = freq.bounds or (sig.bounds is null and freq.bounds is null))
    and (sig.count = freq.count or (sig.count is null and freq.count is null))
    and (sig.as_needed = freq.as_needed or (sig.as_needed is null and freq.as_needed is null))