# Testing

> [!NOTE]
> Return back to the [README.md](/README.md) file.

### Python

I have used the [PEP8 Code Institute Validator](https://pep8ci.herokuapp.com/) to validate all of my py files.

| Directory | File | URL | Screenshot |
| --- | --- | --- | --- |
| projects | projects-forms.py | --- | ![screenshot](./documentation/test_reports/projects_app_linted/projects_forms_CI_linted.png) |
| projects | projects-models.py | --- | ![screenshot](./documentation/test_reports/projects_app_linted/projects_models_CI_linted.png) |
| projects | projects-test_projects_buttons.py | --- | ![screenshot](./documentation/test_reports/projects_app_linted/projects_test_project_buttons_CI_linted.png) |
| projects | projects-tests.py | --- | ![screenshot](./documentation/test_reports/projects_app_linted/projects_tests_CI_linted.png) |
| projects | projects-urls.py | --- | ![screenshot](./documentation/test_reports/projects_app_linted/projects_urls_CI_linted.png) |
| projects | projects-views.py | --- | ![screenshot](./documentation/test_reports/projects_app_linted/projects_views_CI_linted.png) |
| tasks | tasks-forms.py | --- | ![screenshot](./documentation/test_reports/tasks_app_linted/tasks_forms_CI_linted.png) |
| tasks | tasks-models.py | --- | ![screenshot](./documentation/test_reports/tasks_app_linted/tasks_models_CI_linted.png) |
| tasks | tasks-test_tasks_buttons.py | --- | ![screenshot](./documentation/test_reports/tasks_app_linted/tasks_test_tasks_buttons_CI_linted.png) |
| tasks | tasks-tests.py | --- | ![screenshot](./documentation/test_reports/tasks_app_linted/tasks_tests_CI_linted.png) |
| tasks | tasks-urls.py | --- | ![screenshot](./documentation/test_reports/tasks_app_linted/tasks_urls_CI_linted.png) |
| tasks | tasks-views.py | --- | ![screenshot](./documentation/test_reports/tasks_app_linted/tasks_views_CI_linted.png) |
| users | users-backends.py | --- | ![screenshot](./documentation/test_reports/users_app_linted/users_backends_CI_linted.png) |
| users | users-forms.py | --- | ![screenshot](./documentation/test_reports/users_app_linted/users_forms_CI_linted.png) |
| users | users-test_users.py | --- | ![screenshot](./documentation/test_reports/users_app_linted/users_test_users_CI_linted.png) |
| users | users-tests.py | --- | ![screenshot](./documentation/test_reports/users_app_linted/users_tests_CI_linted.png) |
| users | users-urls.py | --- | ![screenshot](./documentation/test_reports/users_app_linted/users_urls_CI_linted.png) |
| users | users-views.py | --- | ![screenshot](./documentation/test_reports/users_app_linted/users_views_CI_linted.png) |

### CSS

I have used the [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator) to validate all of my CSS files.

| Directory | File | URL | Screenshot |
| --- | --- | --- | --- |
| static | assets/stylesheets/authentication.css | --- | ![screenshot](./documentation/test_reports/stylesheets_linted/css_authentication_w3c_linted.png) |
| static | assets/stylesheets/base.css | --- | ![screenshot](./documentation/test_reports/stylesheets_linted/css_base_w3c_linted.png) |
| static | assets/stylesheets/components.css | --- | ![screenshot](./documentation/test_reports/stylesheets_linted/css_components_w3c_linted.png) |
| static | assets/stylesheets/homepage.css | --- | ![screenshot](./documentation/test_reports/stylesheets_linted/css_homepage_w3c_linted.png) |

## Responsiveness

I've tested my deployed project to check for responsiveness issues.

| Page | Mobile | Tablet | Desktop | Notes |
| --- | --- | --- | --- | --- |
| Homepage | ![screenshot](./documentation/responsive/pms-homepage-responsive-mobile.png) | ![screenshot](./documentation/responsive/pms-homepage-responsive-tablet.png) | ![screenshot](./documentation/responsive/pms-homepage-responsive-laptop.png) | Works as expected |
| Login and Register | ![screenshot](./documentation/responsive/pms-login-register-responsive-mobile.png) | ![screenshot](./documentation/responsive/pms-login-register-responsive-tablet.png) | ![screenshot](./documentation/responsive/pms-login-register-responsive-laptop.png) | Works as expected |
| Projects list | ![screenshot](./documentation/responsive/pms-projects-list-responsive-mobile.png) | ![screenshot](./documentation/responsive/pms-projects-list-responsive-tablet.png) | ![screenshot](./documentation/responsive/pms-projects-list-responsive-laptop.png) | Works as expected |

## Browser Compatibility

I've tested my deployed project on multiple browsers to check for compatibility issues.

| Browser | Homepage | Login/Register | Projects |
| --- | --- | --- | --- |
| Google | ![screenshot](./documentation/browser/google.png) | ![screenshot](./documentation/browser/google-login.png) | ![screenshot](./documentation/browser/google-projects.png) | Works as expected |
| Firefox | ![screenshot](./documentation/browser/firefox.png) | ![screenshot](./documentation/browser/firefox-login.png) | ![screenshot](./documentation/browser/firefox-projects.png) | Works as expected |

## Lighthouse Audit

| Page | Mobile | Desktop |
| --- | --- | --- |
| Homepage | ![screenshot](./documentation/lighthouse/mobile/pms-lighthouse-homepage-mobile.png) | ![screenshot](./documentation/lighthouse/desktop/pms-lighthouse-homepage-desktop.png) |
| Login and Register | ![screenshot](./documentation/lighthouse/mobile/pms-lighthouse-loginandregister-mobile.png) | ![screenshot](./documentation/lighthouse/desktop/pms-lighthouse-loginandregister-desktop.png) |
| Projects | ![screenshot](./documentation/lighthouse/mobile/pms-lighthouse-projects-mobile.png) | ![screenshot](./documentation/lighthouse/desktop/pms-lighthouse-projects-desktop.png) |
| Tasks | ![screenshot](./documentation/lighthouse/mobile/pms-lighthouse-tasks-mobile.png) | ![screenshot](./documentation/lighthouse/desktop/pms-lighthouse-tasks-desktop.png) |


# Testing Report

## Overview

I used my created tests.py files to run application tests:

- **Total tests run:** 38  
- **Test duration:** ~50 seconds  
- **Test result:** All tests passed (OK)  

## My tests.py files can be found on the following links :-
- **Projects** [tests.py](./projects/tests.py)
- **Tasks** [tests.py](./tasks/tests.py)
- **Users** [tests.py](./users/tests.py)

# Test Reports

## I have wrote separate functionality tests to test all the buttons in the project, task and user apps.

**You can view the full test report here:**
| Function Test Report | Screenshot |
| --- | --- |
| Html Report | ![screenshot](./documentation/test_reports/test_results_report_html_screenshots.png) |

