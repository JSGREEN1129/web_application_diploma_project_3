import pytest
from django.urls import reverse
from playwright.sync_api import Page

@pytest.mark.django_db
def test_register_create_edit_delete_task(live_server, page: Page):
    """
    End-to-end Playwright test:
    1. Registers a new user
    2. Logs in
    3. Creates a project via UI
    4. Creates a task for that project via UI
    5. Edits the task
    6. Completes the task
    7. Filters tasks
    8. Goes back to projects
    9. Deletes the task
    """
    email = "testuser@example.com"
    password = "Str0ngP@ssw0rd123!"

    # -------------------- REGISTER --------------------
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

    page.wait_for_url(f"{live_server.url}/projects/")
    assert "Projects" in page.content(), "Project list page did not load"

    # -------------------- CREATE PROJECT --------------------
    page.get_by_role("link", name="+ New Project").click()
    page.wait_for_selector("h2", state="visible")
    assert "Create" in page.text_content("h2"), "Not on the create project page"

    project_name = "Playwright Project"
    page.fill('input[name="name"]', project_name)
    page.fill('textarea[name="description"]', "Created via Playwright test")
    page.fill('input[name="start_date"]', "2026-10-28")
    page.fill('input[name="end_date"]', "2026-11-15")
    page.select_option('select[name="status"]', "open")
    page.click('button[type="submit"]')

    page.wait_for_url(f"{live_server.url}{reverse('project_list')}")
    assert project_name in page.content(), "New project not found on list page"

    # -------------------- VIEW PROJECT DETAILS --------------------
    project_card = page.locator("div.card", has_text=project_name)
    project_card.get_by_role("link", name="View Details").click()

    project_detail_url = page.url
    assert f"/projects/" in project_detail_url, "Not on project detail page"

    # -------------------- CREATE TASK --------------------
    page.get_by_role("link", name="+ Add Task").click()
    page.wait_for_selector("h2", state="visible")
    assert "Create" in page.text_content("h2"), "Not on create task page"

    task_name = "Playwright Task"
    page.fill('input[name="name"]', task_name)
    page.fill('textarea[name="description"]', "Task created via Playwright test")
    page.fill('input[name="start_date"]', "2026-10-29")
    page.fill('input[name="end_date"]', "2026-11-10")
    page.select_option('select[name="status"]', "outstanding")
    page.click('button[type="submit"]')

    page.wait_for_selector(f'div.card:has-text("{task_name}")', state="visible")
    assert task_name in page.content(), "Task not found on project detail page"

    # -------------------- EDIT TASK --------------------
    task_card = page.locator("div.card", has_text=task_name)
    task_card.get_by_role("link", name="Edit").click()
    page.wait_for_selector("h3:has-text('Edit Task')", state="visible")

    new_task_name = "Updated Playwright Task"
    page.fill('input[name="name"]', new_task_name)
    page.click('button[type="submit"]')

    page.wait_for_selector(f'div.card:has-text("{new_task_name}")', state="visible")
    assert new_task_name in page.content(), "Task update failed"

    # -------------------- COMPLETE TASK --------------------
    task_card = page.locator("div.card", has_text=new_task_name)
    complete_button = task_card.get_by_role("link", name="Complete")
    page.once("dialog", lambda dialog: dialog.accept())  # accept confirm dialog
    complete_button.click()

    # Wait for "Completed" badge to appear
    task_card.locator('span.badge:has-text("Completed")').wait_for(state="visible")
    assert task_card.locator('span.badge:has-text("Completed")').is_visible()

    # -------------------- FILTER TASKS --------------------
    page.get_by_role("link", name="Completed").click()
    page.wait_for_function("window.location.href.includes('status=completed')")

    # Wait for the completed task to appear
    completed_task_card = page.locator(f'div.card:has-text("{new_task_name}")')
    completed_task_card.wait_for(state="visible", timeout=10000)
    assert completed_task_card.locator('span.badge:has-text("Completed")').is_visible()

    # -------------------- BACK TO PROJECTS --------------------
    page.get_by_role("link", name="Back to Projects").click()
    page.wait_for_url(f"{live_server.url}{reverse('project_list')}")
    assert project_name in page.content(), "Did not navigate back to projects"

    # -------------------- DELETE TASK --------------------
    # Navigate back to the project detail page
    project_card = page.locator("div.card", has_text=project_name)
    project_card.get_by_role("link", name="View Details").click()
    page.wait_for_selector("h2", state="visible")  # ensure page loaded

    # Make sure all tasks are visible
    all_tasks_link = page.get_by_role("link", name="All")
    if all_tasks_link.is_visible():
        all_tasks_link.click()
        page.wait_for_selector(f'div.card:has-text("{new_task_name}")', state="visible")

    # Locate the task card
    task_card = page.locator(f'div.card:has-text("{new_task_name}")')
    task_card.wait_for(state="visible", timeout=15000)

    # Click the "Delete" button that opens the modal
    delete_button = task_card.locator('button[data-bs-toggle="modal"]')
    delete_button.wait_for(state="visible", timeout=10000)
    delete_button.click()

    # Wait for the modal to appear
    modal = page.locator('#deleteTaskModal1')  # adjust selector if your modal ID is different
    modal.wait_for(state="visible", timeout=5000)

    # Fill the password inside the modal
    modal.locator('input[name="password"]').fill(password)

    # Click the confirm "Delete Task" button in the modal
    modal.locator('button.btn-danger:has-text("Delete Task")').click()

    # Wait for the task card to be removed from the page
    task_card.wait_for(state="detached", timeout=10000)

    # Verify the task no longer exists
    assert page.locator(f'div.card:has-text("{new_task_name}")').count() == 0
