﻿note
	description: "Summary description for {SHARED_MIME}."
	author: ""
	date: "$Date$"
	revision: "$Revision$"

class
	SHARED_MIME

feature

	mime: MIME_PARSE
		once
			create Result
		end

	common: COMMON_ACCEPT_HEADER_PARSER
		-- Charset and Encoding
		once
			create Result
		end

	language: LANGUAGE_PARSE
		once
			create Result
		end



end
