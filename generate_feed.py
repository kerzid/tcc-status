
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import format_datetime

# Website information
SITE_URL = "https://kerzid.github.io/tcc-status/"
STATUS_URL = "https://thecoarsecurse.crd.co/#status"

# Read announcements
with open("updates.json", "r", encoding="utf-8") as file:
    updates = json.load(file)

# Sort newest first
updates.sort(
    key=lambda item: datetime.fromisoformat(item["date"]),
    reverse=True
)

# Build RSS document
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")

ET.SubElement(channel, "title").text = (
    "The Coarse Curse - Status Updates"
)
ET.SubElement(channel, "link").text = STATUS_URL
ET.SubElement(channel, "description").text = (
    "Announcements and development updates for The Coarse Curse."
)
ET.SubElement(channel, "language").text = "en-us"

# Feed artwork
image = ET.SubElement(channel, "image")
ET.SubElement(image, "url").text = SITE_URL + "favicon.png"
ET.SubElement(image, "title").text = "The Coarse Curse"
ET.SubElement(image, "link").text = STATUS_URL

# Add announcements
for update in updates:
    item = ET.SubElement(channel, "item")

    ET.SubElement(item, "title").text = update["title"]
    ET.SubElement(item, "link").text = update.get("link", STATUS_URL)
    ET.SubElement(item, "description").text = update["description"]

    guid = ET.SubElement(item, "guid", isPermaLink="false")
    guid.text = update["id"]

    date = datetime.fromisoformat(update["date"])
    if date.tzinfo is None:
        raise ValueError(
            f"Missing timezone in date for: {update['title']}"
        )

    ET.SubElement(item, "pubDate").text = format_datetime(
        date.astimezone(timezone.utc)
    )

# Write RSS file
tree = ET.ElementTree(rss)
ET.indent(tree, space="  ")

tree.write(
    "rss.xml",
    encoding="UTF-8",
    xml_declaration=True
)

print(f"Successfully generated RSS feed with {len(updates)} updates!")
