import pytest
from django.urls import reverse
from playwright.sync_api import Page, expect


@pytest.mark.django_db
def test_users(live_server, page: Page):
    """
    Test registering a new user (auto-login), logging out, and logging back in.
    Verifies that the user's name appears after login.
    """
    # Test user credentials
    first_name = "New"
    last_name = "User"
    email = "newuser@example.com"
    password = "Str0ngP@ssw0rd123!"

    # -------------------- REGISTER --------------------
    page.goto(f"{live_server.url}{reverse('login')}")

    # Switch to Register tab
    register_tab = page.locator('#pills-register-tab')
    if register_tab.get_attribute("aria-selected") != "true":
        register_tab.click()

    # Wait for tab content to be visible
    register_content = page.locator('#pills-register')
    expect(register_content).to_be_visible(timeout=5000)

    # Fill inputs
    first_name_input = register_content.locator('input[name="first_name"]')
    last_name_input = register_content.locator('input[name="last_name"]')
    email_input = register_content.locator('input[name="email"]')
    password1_input = register_content.locator('input[name="password1"]')
    password2_input = register_content.locator('input[name="password2"]')

    # Wait until each input is visible before filling
    for input_field, value in zip(
        [first_name_input, last_name_input,
         email_input, password1_input, password2_input],
        [first_name, last_name, email, password, password],
    ):
        expect(input_field).to_be_visible(timeout=5000)
        input_field.scroll_into_view_if_needed()
        input_field.fill(value)

    # Click register button
    register_btn = page.locator('button[name="register_submit"]')
    expect(register_btn).to_be_enabled(timeout=5000)
    register_btn.click()

    # Confirm auto-login: redirected to projects page
    page.wait_for_url(f"{live_server.url}{reverse('project_list')}")
    assert (
        "Projects" in page.content()
    ), "User was not logged in automatically after registration"

    assert (
        first_name in page.content()
    ), "Logged-in user's name not displayed after registration"

    # -------------------- LOGOUT --------------------
    logout_link = page.get_by_role("link", name="Logout")
    expect(logout_link).to_be_visible(timeout=5000)
    logout_link.click()

    page.wait_for_url(f"{live_server.url}{reverse('login')}")
    assert (
        "Login" in page.content()
    ), "Logout failed or did not redirect to login page"

    # -------------------- LOGIN --------------------
    username_input = page.locator('input[name="username"]')
    password_input = page.locator('input[name="password"]')
    login_btn = page.locator('button[name="login_submit"]')

    expect(username_input).to_be_visible(timeout=10000)
    expect(password_input).to_be_visible(timeout=10000)
    expect(login_btn).to_be_enabled(timeout=10000)

    username_input.fill(email)
    password_input.fill(password)
    login_btn.click()

    page.wait_for_url(f"{live_server.url}{reverse('project_list')}")

    assert (
        "Projects" in page.content()
    ), "Login failed with the newly created user"

    assert (
        first_name in page.content()
    ), "Logged-in user's name not displayed after login"
