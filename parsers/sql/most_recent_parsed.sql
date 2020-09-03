select *
from sig_sig sig
left join sig_sigparsed sig_parsed on sig.id = sig_parsed.sig_id
	and sig_parsed.id =
    	(
            select max(id)
            from sig_sigparsed sp
            where sp.sig_id = sig.id
        )