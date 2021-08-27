from user_agents import parse
import httpx


def get_device_type(user_agent: str):
    device = parse(user_agent)
    return str(device)


async def get_country(request: str):
    async with httpx.AsyncClient() as client:
        try:
            ip_address = request.client.host
            country = await request.app.state.redis.get(ip_address)
            if not country:
                res = await client.get(f"https://ipinfo.io/{ip_address}/json")
                if res.status_code == 200:
                    country = res.json().get("country", "Not defined")
            await request.app.state.redis.set(ip_address, country)
            return country
        except Exception:
            return "Not defined"
