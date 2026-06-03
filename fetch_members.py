import discord
import json
import asyncio
import os
from datetime import datetime

# ── CONFIG ──────────────────────────────────────────────────────────────────
#Name needs to be the exact same as the discord role
# If a rank doesn't have a Discord role, remove it from the dict.
RANK_TO_ROLE = {
    "PVT":  "PVT | Private",
    "PV2":  "PV2 | Private Second Class",
    "PFC":  "PFC | Private First Class",
    "SPC":  "SPC | Specialist",
    "CPL":  "CPL | Corporal",
    "SGT":  "SGT | Sergeant",
    "SSG":  "SSG | Staff Sergeant",
    "SFC":  "SFC | Sergeant First Class",
    "MSG":  "MSG | Master Sergeant",
    "1SG":  "1SG | First Sergeant",
    "SGM":  "SGN | Sergeant Major",
    "CSM":  "CSM | Command Sergeant Major",
    "SMA":  "SMA | Sergeant Major of the Army",
    "WO1":  "WO 1 | Warrant Officer 1",
    "CW2":  "CW2 | Chief Warrant Officer 2",
    "CW3":  "CW3 | Chief Warrant Officer 3",
    "CW4":  "CW4 | Chief Warrant Officer 4",
    "CW5":  "CW5 | Chief Warrant Officer 5",
    "2LT":  "2LT | Second Lieutenant",
    "1LT":  "1LT | First Lieutenant",
    "CPT":  "CPT | Captain",
    "MAJ":  "MAJ | Major",
    "LTC":  "LTC | Lieutenant Colonel",
    "COL":  "COL | Colonel",
    "BG":   "Brigadier General",
    "MG":   "Major General",
    "LTG":  "Lieutenant General",
    "GEN":  "General",
    "GA":   "General of the National Guard",
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
            members = [m.display_name for m in guild.members if role in m.roles]
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
