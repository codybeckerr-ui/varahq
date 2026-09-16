from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .models import AssetTemplate, Organization, UserProfile


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    )
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size=size)
    return ImageFont.load_default()


def _centered(draw: ImageDraw.ImageDraw, text: str, y: int, font: ImageFont.ImageFont, fill: str, width: int) -> None:
    box = draw.textbbox((0, 0), text, font=font)
    draw.text(((width - (box[2] - box[0])) / 2, y), text, font=font, fill=fill)


def _brand_mark(draw: ImageDraw.ImageDraw, organization: Organization, width: int) -> None:
    draw.rounded_rectangle((60, 55, 132, 127), radius=18, outline=organization.accent_color, width=8)
    draw.text((155, 62), organization.brand_name.upper(), font=_font(36, True), fill=organization.accent_color)


def render_asset(template: AssetTemplate, organization: Organization, user: UserProfile) -> Image.Image:
    image = Image.new("RGB", (template.width, template.height), organization.background_color)
    draw = ImageDraw.Draw(image)
    navy = organization.primary_color
    gold = organization.accent_color
    cream = organization.background_color

    if template.layout == "for_sale":
        draw.rectangle((0, 0, template.width, template.height), fill=navy)
        draw.polygon(
            [(template.width * 0.76, 0), (template.width, 0), (template.width, template.height * 0.5), (template.width * 0.76, template.height)],
            fill=cream,
        )
        _brand_mark(draw, organization, template.width)
        draw.text((90, 280), "FOR\nSALE", font=_font(150, True), fill=cream, spacing=0)
        draw.text((95, 665), user.display_name.upper() or "AGENT NAME", font=_font(56, True), fill=gold)
        draw.text((95, 745), user.phone or "PHONE NUMBER", font=_font(62, True), fill=cream)
        draw.text((95, 835), user.job_title or "REALTOR®", font=_font(30), fill=cream)
        if user.license_number:
            draw.text((95, 885), f"License {user.license_number}", font=_font(24), fill=cream)
    else:
        draw.rectangle((0, 0, template.width, template.height), fill=navy)
        top_color = "#D9C6A1" if template.layout == "guide_buyer" else "#8D765B"
        draw.rectangle((0, 0, template.width, int(template.height * 0.58)), fill=top_color)
        for offset in range(0, template.width, 120):
            draw.line((offset, 0, offset + 360, int(template.height * 0.58)), fill="#E8D7B6", width=10)
        _brand_mark(draw, organization, template.width)
        title = "BUYER'S\nGUIDE" if template.layout == "guide_buyer" else "SELLER'S\nGUIDE"
        draw.text((85, int(template.height * 0.64)), title, font=_font(118, True), fill=cream, spacing=-8)
        draw.text((90, int(template.height * 0.88)), f"PREPARED FOR YOU BY {user.display_name.upper()}", font=_font(28, True), fill=gold)
        draw.text((90, int(template.height * 0.925)), user.email, font=_font(25), fill=cream)

    return image


def image_bytes(image: Image.Image, output_format: str) -> bytes:
    buffer = BytesIO()
    if output_format.upper() == "PDF":
        image.convert("RGB").save(buffer, format="PDF", resolution=300.0)
    else:
        image.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()

