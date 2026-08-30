"""Reserved for refrigerator AIHome mode mappings.

No refrigerator select entity is exposed until a real device capture confirms
the command names and parameter values.
"""


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Keep the platform ready without exposing unverified controls."""
    async_add_entities([])
