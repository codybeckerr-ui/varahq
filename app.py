from __future__ import annotations

import streamlit as st

from vara.repository import DemoRepository, RepositoryError, build_repository
from vara.ui import apply_styles, platform_sidebar


st.set_page_config(page_title="Vara — Brand assets, governed", page_icon="V", layout="wide")
apply_styles()


@st.cache_resource
def repository():
    return build_repository()


@st.cache_data(ttl=60)
def load_platform_data():
    repo = repository()
    return repo.get_organization(), repo.get_user(), repo.list_templates(), repo.mode


try:
    pilot_organization, pilot_user, templates, data_mode = load_platform_data()
except RepositoryError as exc:
    st.warning(f"Notion is unavailable, so Vara is using local pilot data. {exc}")
    fallback = DemoRepository()
    pilot_organization, pilot_user, templates, data_mode = (
        fallback.get_organization(),
        fallback.get_user(),
        fallback.list_templates(),
        fallback.mode,
    )

if "surface" not in st.session_state:
    st.session_state.surface = "website"


def open_platform() -> None:
    st.session_state.surface = "platform"


def open_website() -> None:
    st.session_state.surface = "website"


def website() -> None:
    logo, navigation, action = st.columns((1.1, 3.4, 1.15), vertical_alignment="center")
    with logo:
        st.markdown('<div class="vara-wordmark">VARA<span>HQ</span></div>', unsafe_allow_html=True)
    with navigation:
        st.markdown(
            '<div class="vara-nav">Platform&nbsp;&nbsp;&nbsp;&nbsp;Solutions&nbsp;&nbsp;&nbsp;&nbsp;Security&nbsp;&nbsp;&nbsp;&nbsp;Company</div>',
            unsafe_allow_html=True,
        )
    with action:
        if st.button("Open platform →", type="primary", width="stretch"):
            open_platform()
            st.rerun()

    st.markdown(
        """
        <section class="vara-hero">
          <div class="vara-pill">DIGITAL ASSET MANAGEMENT FOR DISTRIBUTED TEAMS</div>
          <h1>Every asset on-brand.<br><em>Every time.</em></h1>
          <p>Vara gives organizations one governed system for creating, personalizing,
          and delivering brand-approved marketing assets at scale.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    hero_left, hero_right = st.columns((1, 1), gap="large", vertical_alignment="center")
    with hero_left:
        a, b = st.columns(2)
        with a:
            if st.button("Explore the platform", type="primary", width="stretch"):
                open_platform()
                st.rerun()
        with b:
            st.button("Book a demo", width="stretch", disabled=True, help="Demo scheduling comes after the pilot.")
        st.caption("Built first for real estate teams. Designed to expand wherever brand compliance matters.")
    with hero_right:
        st.markdown(
            """
            <div class="vara-product-preview">
              <div class="preview-top"><b>Vara Platform</b><span>● Live</span></div>
              <div class="preview-grid">
                <div><small>ORGANIZATIONS</small><strong>1</strong></div>
                <div><small>APPROVED TEMPLATES</small><strong>3</strong></div>
                <div><small>ACTIVE USERS</small><strong>1</strong></div>
                <div><small>RENDER SUCCESS</small><strong>—</strong></div>
              </div>
              <div class="preview-row"><i></i><span>Excelsior Realty</span><b>Pilot</b></div>
              <div class="preview-row"><i></i><span>Template governance</span><b>Ready</b></div>
              <div class="preview-row"><i></i><span>Digital delivery</span><b>Ready</b></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="vara-section-label">THE VARA SYSTEM</div>', unsafe_allow_html=True)
    st.header("One platform from brand rules to final download")
    cards = st.columns(4)
    content = (
        ("01", "Organize", "Centralize organizations, people, templates, and brand rules."),
        ("02", "Govern", "Lock approved artwork while exposing only safe, editable fields."),
        ("03", "Personalize", "Merge approved user data into versioned templates automatically."),
        ("04", "Deliver", "Generate traceable PNG and PDF assets through secure downloads."),
    )
    for column, (number, title, body) in zip(cards, content):
        with column:
            st.markdown(
                f'<div class="vara-feature"><small>{number}</small><h3>{title}</h3><p>{body}</p></div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="vara-callout">
          <div><small>PLATFORM FOUNDATION</small><h2>Start with governance. Add client branding second.</h2></div>
          <p>Vara's base platform owns tenant configuration, template versions, user profiles,
          rendering rules, audit records, and delivery. Client portals become controlled views of that system.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_row() -> None:
    columns = st.columns(4)
    columns[0].metric("Organizations", "1", "1 pilot")
    columns[1].metric("Users", "1", "1 active")
    columns[2].metric("Templates", str(len(templates)), "Seed library")
    columns[3].metric("Renders this month", "0", "Awaiting first asset")


def overview() -> None:
    st.markdown('<div class="vara-eyebrow">PLATFORM OVERVIEW</div>', unsafe_allow_html=True)
    st.title("Good morning, Cody")
    st.caption("Manage the Vara system before configuring individual client experiences.")
    metric_row()
    st.markdown("### Platform readiness")
    left, right = st.columns((1.35, 1), gap="large")
    with left:
        rows = (
            ("Core data model", "Ready", "Organizations, users, templates, fields, rules, and assets"),
            ("Rendering engine", "Ready", "PNG and PDF generation verified"),
            ("Notion connection", "Configuration", "Integration token still required by the app"),
            ("Cloud storage", "Not started", "R2 credentials and signed downloads pending"),
            ("Authentication", "Not started", "Production identity provider pending"),
        )
        for name, status, detail in rows:
            st.markdown(
                f'<div class="platform-row"><div><b>{name}</b><small>{detail}</small></div><span>{status}</span></div>',
                unsafe_allow_html=True,
            )
    with right:
        st.markdown(
            f"""
            <div class="vara-panel">
              <div class="vara-section-label">PILOT TENANT</div>
              <h3>{pilot_organization.name}</h3>
              <p>The first organization record exists as pilot data. Its branded portal remains intentionally deferred.</p>
              <div class="preview-row"><i></i><span>Primary user</span><b>{pilot_user.display_name}</b></div>
              <div class="preview-row"><i></i><span>Profile completion</span><b>{pilot_user.completeness}%</b></div>
              <div class="preview-row"><i></i><span>Data mode</span><b>{data_mode}</b></div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def organizations() -> None:
    st.markdown('<div class="vara-eyebrow">TENANT MANAGEMENT</div>', unsafe_allow_html=True)
    st.title("Organizations")
    st.caption("Organizations are isolated tenants. Their visual portals are generated from the Vara platform configuration.")
    st.dataframe(
        [{"Organization": pilot_organization.name, "Slug": pilot_organization.slug, "Stage": "Pilot", "Users": 1, "Templates": len(templates), "Portal": "Not configured"}],
        hide_index=True,
        width="stretch",
    )
    st.info("Client branding and portal configuration stay out of scope until the Vara platform foundation is complete.")


def users() -> None:
    st.markdown('<div class="vara-eyebrow">IDENTITY DIRECTORY</div>', unsafe_allow_html=True)
    st.title("Users")
    st.caption("Vara manages user-to-organization assignments and approved profile data. Authentication will be delegated to a dedicated provider.")
    st.dataframe(
        [{"Name": pilot_user.display_name, "Email": pilot_user.email, "Organization": pilot_organization.name, "Role": "Broker Admin", "Status": "Active", "Profile": f"{pilot_user.completeness}%"}],
        hide_index=True,
        width="stretch",
    )


def template_system() -> None:
    st.markdown('<div class="vara-eyebrow">TEMPLATE SYSTEM</div>', unsafe_allow_html=True)
    st.title("Template registry")
    st.caption("The registry governs template versions, output sizes, allowed formats, and configurable fields before any client portal displays them.")
    st.dataframe(
        [{"Template": template.name, "Category": template.category, "Version": template.version, "Canvas": f"{template.width} × {template.height}", "Formats": ", ".join(template.formats), "Status": "Seed example"} for template in templates],
        hide_index=True,
        width="stretch",
    )
    st.warning("These are renderer test fixtures—not approved Excelsior assets.")


def render_operations() -> None:
    st.markdown('<div class="vara-eyebrow">RENDER OPERATIONS</div>', unsafe_allow_html=True)
    st.title("Generated assets")
    st.caption("Every generation request will be recorded with tenant, user, template version, input snapshot, checksum, and output location.")
    st.markdown('<div class="vara-empty"><b>No render jobs yet</b><p>The audit stream will appear here after the base API and storage layer are connected.</p></div>', unsafe_allow_html=True)


def system_settings() -> None:
    st.markdown('<div class="vara-eyebrow">SYSTEM</div>', unsafe_allow_html=True)
    st.title("Platform configuration")
    st.caption("Connection status for the services Vara will use across every tenant.")
    settings = (
        ("Notion", "Demo mode" if data_mode == "Demo" else "Connected", "Configuration and pilot operations"),
        ("Cloudflare R2", "Not connected", "Source templates and generated assets"),
        ("Authentication", "Not connected", "Tenant identity and session security"),
        ("Renderer", "Local", "Pillow-based PNG and PDF output"),
    )
    for service, status, purpose in settings:
        st.markdown(f'<div class="platform-row"><div><b>{service}</b><small>{purpose}</small></div><span>{status}</span></div>', unsafe_allow_html=True)


if st.session_state.surface == "website":
    website()
else:
    section = platform_sidebar(open_website)
    if section == "Overview":
        overview()
    elif section == "Organizations":
        organizations()
    elif section == "Users":
        users()
    elif section == "Templates":
        template_system()
    elif section == "Render Operations":
        render_operations()
    else:
        system_settings()
