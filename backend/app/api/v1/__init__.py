from fastapi import APIRouter

from app.api.v1 import (
    admin_audit_log,
    admin_auth,
    admin_community,
    admin_dashboard,
    admin_education,
    admin_events,
    admin_experience,
    admin_homepage,
    admin_media,
    admin_navigation,
    admin_profile,
    admin_projects,
    admin_recognition,
    admin_redirects,
    admin_search,
    admin_site_settings,
    admin_skills,
    admin_social_links,
    admin_system,
    admin_tags,
    biography,
    community,
    contact,
    education,
    events,
    experiences,
    homepage,
    journey,
    media,
    navigation,
    passions,
    profile,
    projects,
    recognition,
    redirects,
    site_settings,
    skills,
    social_links,
    talks,
)

router = APIRouter()
router.include_router(profile.router, tags=["profile"])
router.include_router(biography.router, tags=["profile"])
router.include_router(education.router, tags=["education"])
router.include_router(journey.router, tags=["journey"])
router.include_router(experiences.router, tags=["experience"])
router.include_router(projects.router, tags=["projects"])
router.include_router(skills.router, tags=["skills"])
router.include_router(events.router, tags=["events"])
router.include_router(talks.router, tags=["talks"])
router.include_router(passions.router, tags=["passions"])
router.include_router(community.router, tags=["community"])
router.include_router(recognition.router, tags=["recognition"])
router.include_router(media.router, tags=["media"])
router.include_router(navigation.router, tags=["navigation"])
router.include_router(social_links.router, tags=["social-links"])
router.include_router(redirects.router, tags=["redirects"])
router.include_router(site_settings.router, tags=["site-settings"])
router.include_router(homepage.router, tags=["homepage"])
router.include_router(contact.router, tags=["contact"])
router.include_router(admin_auth.router, tags=["admin-auth"])
router.include_router(admin_events.router, tags=["admin-events"])
router.include_router(admin_projects.router, tags=["admin-projects"])
router.include_router(admin_experience.router, tags=["admin-experience"])
router.include_router(admin_education.router, tags=["admin-education"])
router.include_router(admin_community.router, tags=["admin-community"])
router.include_router(admin_profile.router, tags=["admin-profile"])
router.include_router(admin_recognition.router, tags=["admin-recognition"])
router.include_router(admin_skills.router, tags=["admin-skills"])
router.include_router(admin_media.router, tags=["admin-media"])
router.include_router(admin_navigation.router, tags=["admin-navigation"])
router.include_router(admin_social_links.router, tags=["admin-social-links"])
router.include_router(admin_redirects.router, tags=["admin-redirects"])
router.include_router(admin_site_settings.router, tags=["admin-site-settings"])
router.include_router(admin_homepage.router, tags=["admin-homepage"])
router.include_router(admin_tags.router, tags=["admin-tags"])
router.include_router(admin_dashboard.router, tags=["admin-dashboard"])
router.include_router(admin_audit_log.router, tags=["admin-audit-log"])
router.include_router(admin_system.router, tags=["admin-system"])
router.include_router(admin_search.router, tags=["admin-search"])
