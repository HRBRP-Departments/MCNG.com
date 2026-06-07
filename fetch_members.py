import discord
import json
import asyncio
import os
from datetime import datetime

# ── CONFIG ──────────────────────────────────────────────────────────────────
# Map each rank abbreviation to the EXACT Discord role name in your server.
# If a rank doesn't have a Discord role, remove it from the dict.
RANK_TO_ROLE = {
    # Junior Enlisted
    "PVT":  "PVT",
    "PV2":  "PV2",
    "PFC":  "PFC",
    "SPC":  "SPC",
    # Non-commissioned Officers
    "CPL":  "CPL",
    "SGT":  "SGT",
    "SSG":  "SSG",
    # Senior NCOs
    "SFC":  "SFC",
    "MSG":  "MSG",
    "1SG":  "1SG",
    "SGM":  "SGM",
    "CSM":  "CSM",
    "SMA":  "SMA",
    # Warrant Officers
    "WO1":  "WO1",
    "CW2":  "CW2",
    "CW3":  "CW3",
    "CW4":  "CW4",
    "CW5":  "CW5",
    # Junior Officers
    "2LT":  "2LT",
    "1LT":  "1LT",
    "CPT":  "CPT",
    # Senior Officers
    "MAJ":  "MAJ",
    "LTC":  "LTC",
    "COL":  "COL",
    # General Officers
    "BG":   "BG",
    "MG":   "MG",
    "LTG":  "LTG",
    "GEN":  "GEN",
    "GA":   "GA",
}

# ── NAME OVERRIDES ───────────────────────────────────────────────────────────
# Format: "Discord display name": "Name to show on website"
NAME_OVERRIDES = {
    "CIV | Arrcqne": "GEN | Arrcqne",
}
# ────────────────────────────────────────────────────────────────────────────

TOKEN     = os.environ["DISCORD_TOKEN"]
GUILD_ID  = int(os.environ["DISCORD_GUILD_ID"])

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        print(f"ERROR: Guild {GUILD_ID} not found.")
        await client.close()
        return

    # Build role-name → role object map
    role_map = {r.name: r for r in guild.roles}

    result = {}
    for rank, role_name in RANK_TO_ROLE.items():
        role = role_map.get(role_name)
        if role:
            members = [NAME_OVERRIDES.get(m.display_name, m.display_name) for m in guild.members if role in m.roles]
            result[rank] = sorted(members, key=str.lower)
        else:
            result[rank] = []   # role not found – leave empty

    output = {
        "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "members": result
    }

    with open("members.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅  Saved members.json  ({datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')})")
    await client.close()

client.run(TOKEN)
