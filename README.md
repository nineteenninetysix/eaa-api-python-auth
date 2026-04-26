### Overview

Example of how to use the edge authentication in a python script to interact with the [EAA API](https://techdocs.akamai.com/eaa-api/reference/api).

Included is also an example of how to utilise the authenticated request to perform simple reporting:
- goes through all EAA applications within your account, and deploy all which have pending changes.

_Note:_ This can be limited by setting the `max_apps=` - see the comments in the script for instructions on how to do this.
