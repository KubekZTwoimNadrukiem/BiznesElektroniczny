package com.example;

import java.io.File;
import java.io.IOException;
import java.time.Duration;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.ThreadLocalRandom;
import java.util.stream.IntStream;

import org.junit.jupiter.api.AfterAll;
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;
import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Keys;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.WindowType;
import org.openqa.selenium.chrome.ChromeDriverService;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

@SuppressWarnings("UnnecessaryReturnStatement")
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class MainTest {
    private static ChromeDriverService driverService;
    private static WebDriver webDriver;
    private static WebDriverWait wait;
    private final Keys controlKey = System.getProperty("os.name").contains("Mac OS") ? Keys.COMMAND : Keys.CONTROL;
    @BeforeAll
    public static void createService() throws IOException {
        //xattr -d com.apple.quarantine chromedriver
        driverService = new ChromeDriverService.Builder().usingDriverExecutable(new File("chromedriver")).usingAnyFreePort().build();
        driverService.start();
        ChromeOptions chromeOptions = new ChromeOptions();
        chromeOptions.addArguments("--remote-allow-origins=*");
        //ChromeDriver does not support Chrome v131
        //webDriver = new ChromeDriver(chromeOptions);
        webDriver = new RemoteWebDriver(driverService.getUrl(), new ChromeOptions());
        wait = new WebDriverWait(webDriver, 5);
        return;
    }
    @AfterAll   
    public static void stopService() {
        webDriver.close();
        webDriver.quit();
        driverService.stop();
        return;
    }
    private int openProductsTabs(String category) {
        webDriver.get(category);
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("product-thumbnail")));
        WebElement productList = webDriver.findElement(By.id("js-product-list"));
        int productListSize = productList.findElements(By.className("product-thumbnail")).size();
        int size = Math.min(productListSize, 10);
        for (int i = 0; i < size; i++) {
            wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//div[@id='js-product-list']//div[@class='product-price-and-shipping']//a")));
            productList.findElements(By.xpath("//div[@id='js-product-list']//div[@class='product-price-and-shipping']//a")).get(i).sendKeys(Keys.chord(this.controlKey, Keys.ENTER));
        }
        return size;
    }
    @Order(1)
    @Test
    //TODO change categories
    public void testAddToCart() {
        int numberOfTabs = openProductsTabs("http://localhost:8089/en/3-category1");
        webDriver.switchTo().newWindow(WindowType.TAB);
        numberOfTabs += openProductsTabs("http://localhost:8089/en/4-category2");
        Object windowHandles[] = webDriver.getWindowHandles().toArray();
        int[] quantities = IntStream.rangeClosed(0, 20).map(a -> a % 5 + 1).toArray();
        for (int i = 0, q = 0; i < numberOfTabs + 2; i++, q++) {
            webDriver.switchTo().window((String) windowHandles[i]);
            try {
                webDriver.manage().timeouts().implicitlyWait(Duration.ofSeconds(1));
                webDriver.findElement(By.id("quantity_wanted"));
            } catch (NoSuchElementException e) {
                q--;
                if (i < numberOfTabs + 1) webDriver.close();
                continue;
            }
            wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("quantity_wanted")));
            WebElement input = webDriver.findElement(By.id("quantity_wanted"));
            input.sendKeys(Keys.chord(this.controlKey, "A", Keys.DELETE));
            input.sendKeys(String.valueOf(quantities[q]));
            wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("button.add-to-cart")));
            webDriver.findElement(By.cssSelector("button.add-to-cart")).click();
            try {
                Thread.sleep(Duration.ofSeconds(1));
            } catch (InterruptedException ex) {
            }
            if (i < numberOfTabs + 1) webDriver.close();
        }
        webDriver.navigate().refresh();
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("cart-products-count")));
        int expectedResult = (Arrays.stream(Arrays.copyOf(quantities, numberOfTabs))).sum();
        String result = webDriver.findElement(By.className("cart-products-count")).getText().replaceAll("[()]", "");
        assertEquals(expectedResult, Integer.valueOf(result));
        return;
    }
    @Order(2)
    @Test
    public void testSearchAndAddToCart() {
        webDriver.get("http://localhost:8089/en/");
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("cart-products-count")));
        String expectedResult = webDriver.findElement(By.className("cart-products-count")).getText().replaceAll("[()]", "");
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//div[@id='search_widget']//input[@name='s']")));
        WebElement searchBar = webDriver.findElement(By.xpath("//div[@id='search_widget']//input[@name='s']"));
        searchBar.clear();
        //TODO change product name
        searchBar.sendKeys("student");
        searchBar.sendKeys(Keys.ENTER);
        wait.until(ExpectedConditions.elementToBeClickable(By.xpath("//div[@id='js-product-list']//div[@class='product-price-and-shipping']//a")));
        List<WebElement> productList = webDriver.findElements(By.xpath("//div[@id='js-product-list']//div[@class='product-price-and-shipping']//a"));
        productList.get(ThreadLocalRandom.current().nextInt(productList.size())).click();
        wait.until(ExpectedConditions.elementToBeClickable(By.className("add-to-cart")));
        webDriver.findElement(By.className("add-to-cart")).click();
        try {
            Thread.sleep(Duration.ofSeconds(1));
        } catch (InterruptedException ex) {
        }
        webDriver.navigate().refresh();
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("cart-products-count")));
        String result = webDriver.findElement(By.className("cart-products-count")).getText().replaceAll("[()]", "");
        assertEquals(Integer.parseInt(expectedResult) + 1, Integer.parseInt(result));
        return;
    }
    @Order(3)
    @Test
    //TODO Yarnstreet asks to confirm the deletion of product through an alert window
    public void testRemoveFromCart() {
        webDriver.get("http://localhost:8089/en/cart?action=show");
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("cart-products-count")));
        String cartSize = webDriver.findElement(By.className("cart-products-count")).getText().replaceAll("[()]", "");
        wait.until(ExpectedConditions.elementToBeClickable(By.className("remove-from-cart")));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("js-cart-line-product-quantity")));
        int deleteButtonsSize = webDriver.findElements(By.className("emove-from-cart")).size();
        int size = Math.min(deleteButtonsSize, 3);
        int removed = 0;
        for (int i = 0; i < size; i++) {
            wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("js-cart-line-product-quantity")));
            removed += Integer.parseInt(webDriver.findElement(By.className("js-cart-line-product-quantity")).getAttribute("value"));
            webDriver.findElement(By.className("remove-from-cart")).click();
            webDriver.navigate().refresh();
        }
        webDriver.navigate().refresh();
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("cart-products-count")));
        String result = webDriver.findElement(By.className("cart-products-count")).getText().replaceAll("[()]", "");
        assertEquals(Integer.parseInt(cartSize) - removed,  Integer.parseInt(result));
        return;
    }
    @Order(4)
    @Test
    //TODO Yarnstreet has different fileds (email, password, confirm password)
    public void testCreateAccount(){
        webDriver.get("http://localhost:8089/en/login?create_account=1");
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("field-firstname")));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("field-lastname")));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("field-email")));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("field-password")));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector("button.form-control-submit")));
        //wait.until(ExpectedConditions.visibilityOfElementLocated(By.name("customer_privacy")));
        //wait.until(ExpectedConditions.visibilityOfElementLocated(By.name("psgdpr")));
        webDriver.findElement(By.id("field-firstname")).sendKeys("UserA");
        webDriver.findElement(By.id("field-lastname")).sendKeys("UserA");
        webDriver.findElement(By.id("field-email")).sendKeys(UUID.randomUUID().toString() + "@user");
        webDriver.findElement(By.id("field-password")).sendKeys("12345678");
        webDriver.findElement(By.name("customer_privacy")).click();
        webDriver.findElement(By.name("psgdpr")).click();
        webDriver.findElement(By.cssSelector("button.form-control-submit")).click();
        try {
            Thread.sleep(Duration.ofSeconds(1));
        } catch (InterruptedException ex) {
        }
        assertDoesNotThrow(() -> webDriver.findElement(By.className("account")));
        return;
    }
    @Order(5)
    @Test
    //TODO change delivery and payment options' id
    public void testPlaceOrder() {
        webDriver.get("http://localhost:8089/en/cart?action=show");
        wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("a.btn-primary")));
        webDriver.findElement(By.cssSelector("a.btn-primary")).click();
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("field-address1")));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("field-postcode")));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("field-city")));
        wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("button[name='confirm-addresses']")));
        webDriver.findElement(By.id("field-address1")).sendKeys("Adress");
        webDriver.findElement(By.id("field-postcode")).sendKeys("11-111");
        webDriver.findElement(By.id("field-city")).sendKeys("City");
        webDriver.findElement(By.cssSelector("button[name='confirm-addresses']")).click();
        //wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("delivery_option_1")));
        wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("button[name='confirmDeliveryOption']")));
        JavascriptExecutor jsExecutor = (JavascriptExecutor) webDriver;
        jsExecutor.executeScript("arguments[0].click();", webDriver.findElement(By.id("delivery_option_1")));
        webDriver.findElement(By.cssSelector("button[name='confirmDeliveryOption']")).click();
        //wait.until(ExpectedConditions.elementToBeClickable(By.id("payment-option-1")));
        //wait.until(ExpectedConditions.elementToBeClickable(By.id("conditions_to_approve[terms-and-conditions]")));
        jsExecutor.executeScript("arguments[0].click();", webDriver.findElement(By.id("payment-option-1")));
        webDriver.findElement(By.id("conditions_to_approve[terms-and-conditions]")).click();
        try {
            Thread.sleep(Duration.ofSeconds(1));
        } catch (InterruptedException ex) {
        }
        //wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector("//div[@id='payment-confirmation']//button[@type='submit']")));
        webDriver.findElement(By.xpath("//div[@id='payment-confirmation']//button[@type='submit']")).click();
        try {
            Thread.sleep(Duration.ofSeconds(2));
        } catch (InterruptedException ex) {
        }
        assertDoesNotThrow(() -> webDriver.findElement(By.xpath("//h3[contains(., 'Your order is confirmed')]")));
        return;
    }
    @Order(6)
    @Test
    public void testCheckProductDetails() {
        webDriver.get("http://localhost:8089/en/my-account");
        wait.until(ExpectedConditions.elementToBeClickable(By.id("history-link")));
        webDriver.findElement(By.id("history-link")).click();
        wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("a[data-link-action='view-order-details']")));
        webDriver.findElement(By.cssSelector("a[data-link-action='view-order-details']")).click();
        assertDoesNotThrow(() -> webDriver.findElement(By.id("order-history")));
        return;
    }
    @Order(7)
    @Test
    public void testVATFacture() {
        wait.until(ExpectedConditions.elementToBeClickable(By.cssSelector("a[href*='pdf-invoice']")));
        assertDoesNotThrow(() -> webDriver.findElement(By.cssSelector("a[href*='pdf-invoice']")).click());
        return;
    }
}
