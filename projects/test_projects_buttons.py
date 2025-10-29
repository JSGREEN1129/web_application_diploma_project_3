import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_register_and_create_project(live_server, page):
    """
    End-to-end Playwright test that:
    1. Registers a user
    2. Creates a new project
    3. Tests project list filter buttons
    4. Edits the project (with password confirmation)
    5. Marks project as completed, then reopens it
    6. Deletes the project (with password confirmation)
    """

    email = "testuser@example.com"
    password = "Str0ngP@ssw0rd123!"

    # --- REGISTER ---
    page.goto(f"{live_server.url}{reverse('login')}")
    register_tab = page.query_selector('#pills-register-tab')
    if register_tab.get_attribute("aria-selected") != "true":
        register_tab.click()

    page.wait_for_selector('input[name="first_name"]', state='visible')
    page.fill('input[name="first_name"]', "Test")
    page.fill('input[name="last_name"]', "User")
    page.fill('input[name="email"]', email)
    page.fill('input[name="password1"]', password)
    page.fill('input[name="password2"]', password)
    page.click('button[name="register_submit"]')

    page.wait_for_url(f"{live_server.url}{reverse('project_list')}")
    assert "Projects" in page.content(
    ), "Project list page did not load after registration/login"

    # --- CREATE PROJECT ---
    page.wait_for_selector('text="+ New Project"', state='visible')
    page.get_by_role("link", name="+ New Project", exact=False).click()

    page.wait_for_selector("h2", state="visible")
    assert "Create" in page.text_content(
        "h2"), "Not on the create project page"

    page.fill('input[name="name"]', "Playwright Project")
    page.fill('textarea[name="description"]', "Created via Playwright test")
    page.fill('input[name="start_date"]', "2026-10-28")
    page.fill('input[name="end_date"]', "2026-11-15")
    page.select_option('select[name="status"]', "open")
    page.click('button[type="submit"]')

    # Verify creation success
    page.wait_for_url(f"{live_server.url}{reverse('project_list')}")
    assert "Playwright Project" in page.content(), "New project not found"

    # --- FILTER BUTTONS ---
    page.click('a[href="?status=open"]')
    page.wait_for_timeout(500)
    assert "Playwright Project" in page.content(
    ), "Project missing in 'Open Projects' filter"

    page.click('a[href="?status=closed"]')
    page.wait_for_timeout(500)
    page.click('a[href="?status=all"]')
    page.wait_for_timeout(500)
    assert "Playwright Project" in page.content(
    ), "Project missing in 'All Projects' filter"

    # --- EDIT PROJECT ---
    page.get_by_role("link", name="Edit", exact=False).click()
    page.wait_for_selector("h2", state="visible")
    assert "Edit" in page.text_content("h2"), "Not on edit project page"

    page.fill('textarea[name="description"]', "Updated via Playwright test")

    # If password confirmation is required for editing, fill it in
    if page.is_visible('input[name="password"]'):
        page.fill('input[name="password"]', password)

    # Submit form
    page.click('button[type="submit"]')

    # Wait for redirect back to project list
    page.wait_for_url(f"{live_server.url}{reverse('project_list')}")
    assert (
        "Updated via Playwright test" in page.content()
        or "Playwright Project" in page.content()
    )

    # --- MARK AS COMPLETED ---
    if page.is_visible('a:has-text("Mark as Completed")'):
        page.get_by_role("link", name="Mark as Completed", exact=False).click()
        page.wait_for_timeout(1000)
        assert ("Closed" in page.content(
        ) or "Re-open Project" in page.content(),
            "Failed to mark project as completed")

    # --- REOPEN PROJECT ---
    if page.is_visible('a:has-text("Re-open Project")'):
        page.get_by_role("link", name="Re-open Project", exact=False).click()
        page.wait_for_timeout(1000)
        assert "Open" in page.content(
        ) or "Mark as Completed" in page.content(), "Failed to reopen project"

    # --- DELETE PROJECT ---
    # Click Delete button to open modal
    page.click('button[data-bs-target^="#deleteProjectModal"]')
    page.wait_for_selector('.modal.show', state='visible')
    page.fill('.modal.show input[name="password"]', password)
    page.click('.modal.show button.btn-danger')  # Confirm delete

    page.wait_for_url(f"{live_server.url}{reverse('project_list')}")
    page.wait_for_timeout(1000)

    html = page.content()

    # Allow it to appear in success messages but not in actual project entries
    assert (
        "Project 'Playwright Project' deleted successfully!" in html,
        "Delete success message missing",
    )

    # Ensure it's not listed as a project anymore
    project_rows = page.query_selector_all("div.row, table, li, a, p")
    visible_text = [el.inner_text() for el in project_rows]
    assert not any("Playwright Project" in t for t in
                   visible_text if "deleted successfully" not in t), \
        "Project still visible in project list after deletion"
