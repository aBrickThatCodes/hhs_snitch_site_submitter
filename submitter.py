import random

import faker
from playwright.sync_api import sync_playwright


def company_or_individual():
    return random.choice(
        (
            fake.company() + random.choice((" - organisation", " - business")),
            fake.name() + " - individual",
        )
    )


fake = faker.Faker()

fields = (
    ("#edit-hcp-name", company_or_individual),
    ("#edit-hcp-relationship", fake.job),
    ("#edit-hcp-phone", fake.phone_number),
    ("#edit-hcp-email", fake.free_email),
    ("#edit-hcp-job-title", fake.job),
    ("#edit-hcp-employer", company_or_individual),
    ("#edit-hcp-business-address-address", fake.street_address),
    ("#edit-hcp-business-address-address-2", fake.building_number),
    ("#edit-hcp-business-address-city", fake.city),
    ("#edit-hcp-business-address-postal-code", fake.postalcode),
    ("#edit-your-details-first-name", fake.first_name),
    ("#edit-your-details-last-name", fake.last_name),
    ("#edit-your-details-cell-phone", fake.phone_number),
    ("#edit-your-details-personal-email", fake.free_email),
)


if __name__ == "__main__":
    with sync_playwright() as p:
        print("Submitting, please wait")
        with p.firefox.launch() as browser:
            with browser.new_page() as page:
                page.goto("https://www.hhs.gov/protect-kids/", timeout=0)
                for field, filler in fields:
                    frame = page.frame_locator(field)
                    frame.owner.fill(filler())
                page.get_by_text("No", exact=True).click()
                page.get_by_text(
                    "I wish to remain",
                ).click()
                page.frame_locator(
                    "#edit-hcp-business-address-state-province"
                ).owner.select_option(fake.state())
                page.frame_locator("#edit-submit").owner.click()
                print("Tip submitted")
