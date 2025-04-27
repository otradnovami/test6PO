import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.fixture(scope="function")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

def test_saucedemo_purchase(browser_context):
    page = browser_context.new_page()

    # Авторизация
    page.goto("https://www.saucedemo.com/")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    # Проверка успешной авторизации
    expect(page.locator(".title")).to_have_text("Products")

    # Выбор товара (Sauce Labs Backpack)
    page.click("//div[text()='Sauce Labs Backpack']/../../..//button[text()='Add to cart']")

    # Переход в корзину
    page.click(".shopping_cart_link")

    # Проверка, что товар в корзине
    expect(page.locator(".inventory_item_name")).to_have_text("Sauce Labs Backpack")

    # Переход к оформлению заказа
    page.click("#checkout")

    # Заполнение формы оформления
    page.fill("#first-name", "Will")
    page.fill("#last-name", "Mag")
    page.fill("#postal-code", "830463")
    page.click("#continue")

    # Проверка страницы подтверждения
    expect(page.locator(".title")).to_have_text("Checkout: Overview")
    expect(page.locator(".inventory_item_name")).to_have_text("Sauce Labs Backpack")

    # Завершение покупки
    page.click("#finish")

    # Проверка успешного завершения покупки
    expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")

    page.close()