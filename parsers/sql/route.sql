select * from parserx.sig_sigparsed sig
inner join vumc.route route
	on sig.route = route.route