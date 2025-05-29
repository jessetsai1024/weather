from typing import Any
import httpx
import asyncio
import json

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

async def main() -> None:
    url = "https://api.weather.gov/alerts/active?area=CA"
    data = await make_nws_request(url)

    if data is None:
        print("⚠️  無法取得資料。")
        return

    # 1️⃣ 先印出總筆數
    print(f"共有 {len(data.get('features', []))} 則天氣警報。\n")

    # 2️⃣ 再把整個 GeoJSON 美化後印出
    pretty = json.dumps(data, ensure_ascii=False, indent=2)
    print(pretty)

if __name__ == "__main__":
    asyncio.run(main())