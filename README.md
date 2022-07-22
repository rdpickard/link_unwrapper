# Link unwrapper
Web service to get the URL of links that are obscured by intermediary ad tracking tools such as 'shorteners'. 

Link intermediaries are used by ad companies to track you by acting as middle men between URLs. They provide no value to the consumer of the link (you) and create bloat, delay and security threats by hiding the actual location of a link.

Link Unwrapper is a simple web service with only one API endpoint that takes in a URL from a link shortener and returns the actual URL. The service does no tracking, keeps no records of who requested what link to be unwrapped. It does keep a tempory cache of shortend to full links for effiencey but no user data is stored in the cache. 

This version is intented to run on Heroku. The web service can be run locally for testing but that is likely to expose your IP to the URL shortener service which may weaken the ad tracking protections of Link Unwrapper. Running in the cloud means the unrwapping will be done from a differnet IP (the cloud service's) than the shortened URL was served to (your IP). Getting a running instance on Heroku is pretty easy with github integration. So you can run your own instance.

Ad tech is intentionally opaque so it is not clear to me how much of an impact link unwrapping will have on privacy preservation. This is an experiment.
