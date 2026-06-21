from typing import Any, Dict

import httpx
import urllib

allservers = [
    { "country": "FREE", "url": "https://free.freeipapi.com" },
    # { "country": "US", "url": "https://us.freeipapi.com" },
    # { "country": "DE", "url": "https://de.freeipapi.com" },
    # { "country": "SGP", "url": "https://sgp.freeipapi.com" },
    # { "country": "AU", "url": "https://au.freeipapi.com" }
]

selectedServer = allservers[0]

def selectServer(server: str) -> Dict[str, Any]:
    global selectedServer
    for srv in allservers:
        if srv["country"] == server:
            selectedServer = srv
            return {"message": f"Server '{server}' selected successfully."}
    return {"message": f"Server '{server}' not found."}

def getIPInfo(ip: str) -> Dict[str, Any]:
    try:
        response = httpx.get(urllib.parse.urljoin(selectedServer["url"], f"/api/json/{ip}"))
        response.raise_for_status()
        json = response.json()

        return {
            "IPv": json.get("ipVersion"),
            "IPa": json.get("ipAddress"),
            "Lat": json.get("latitude"),
            "Long": json.get("longitude"),
            "CountryName": json.get("countryName"),
            "CountryCode": json.get("countryCode"),
            "Capital": json.get("capital"),
            "PhoneCodes": json.get("phoneCodes"),
            "TimeZones": json.get("timeZones"),
            "zippy": json.get("zipCode"),
            "city": json.get("city"),
            "Region": json.get("regionName"),
            "RegionCode": json.get("regionCode"),
            "ContinentName": json.get("continent"),
            "ContinentCode": json.get("continentCode"),
            "Currencies": json.get("currencies"),
            "Languages": json.get("languages"),
            "asn": json.get("asn"),
            "asnOrganization": json.get("asnOrganization"),
            "isProxy": json.get("isProxy"),
        }

    except httpx.HTTPError as e:
        return {"message": f"Error fetching IP info: {str(e)}"}