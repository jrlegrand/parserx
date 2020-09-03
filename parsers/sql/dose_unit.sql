select * from parserx.sig_sigparsed sig
inner join vumc.dose_unit dose_unit 
	on coalesce(sig.strength_unit, sig.dose_unit) = dose_unit.dose_unit