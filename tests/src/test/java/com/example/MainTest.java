package com.example;

import java.time.Duration;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.TimeUnit;
import java.util.stream.IntStream;

import org.junit.jupiter.api.AfterEach;
import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.WindowType;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.FluentWait;
import org.openqa.selenium.support.ui.Wait;
import org.openqa.selenium.support.ui.WebDriverWait;

@SuppressWarnings("UnnecessaryReturnStatement")
public class MainTest {
    //private static ChromeDriverService driverService;
    private static WebDriver webDriver;
    private static WebDriverWait wait;

/*
    @BeforeAll
    public static void createService() throws IOException {
        driverService = new ChromeDriverService.Builder().usingDriverExecutable(new File("chromedriver")).usingAnyFreePort().build();
        driverService.start();
        return;
    }
    @AfterAll   
    public static void stopService() {
        driverService.stop();
        return;
    }
*/
 
    @BeforeEach
    public void createDriver() {
        ChromeOptions chromeOptions = new ChromeOptions();
        chromeOptions.addArguments("--remote-allow-origins=*");
        webDriver = new ChromeDriver(chromeOptions);
        //webDriver = RemoteWebDriver(driverService.getUrl(), new ChromeOptions());
        wait = new WebDriverWait(webDriver, 5);
        return;
    }
    @AfterEach
    public void quitDriver() {
        webDriver.close();
        webDriver.quit();
        return;
    }
    private int openProductsTabs(String category) {
        webDriver.get(category);
        webDriver.manage().timeouts().implicitlyWait(Duration.ofSeconds(5));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("product-thumbnail")));
        WebElement productList = webDriver.findElement(By.id("js-product-list"));
        int productListSize = productList.findElements(By.className("product-thumbnail")).size();
        int size = Math.min(productListSize, 10);
        for (int i = 0; i < size; i++) {
            //TODO Keys.COMMAND -> Keys.CONTROL for Windows or Linux
            String newTabShortcut = Keys.chord(Keys.COMMAND, Keys.ENTER);
            wait.until(ExpectedConditions.elementToBeClickable(By.className("product-thumbnail")));
            productList.findElements(By.className("product-thumbnail")).get(i).sendKeys(newTabShortcut);
        }
        return size;
    }
    @Test
    //TODO change categories
    public void testAddToCart() {
        int expectedResult = openProductsTabs("http://localhost:8089/en/3-category1");
        webDriver.switchTo().newWindow(WindowType.TAB);
        expectedResult += openProductsTabs("http://localhost:8089/en/4-category2");
        Object windowHandles[] = webDriver.getWindowHandles().toArray();
        int[] quantities = IntStream.rangeClosed(1, 20).toArray();
        for (int i = 0, q = 0; i < expectedResult + 2; i++, q++) {
            webDriver.switchTo().window((String) windowHandles[i]);
            Wait<WebDriver> shortWait = new FluentWait<>(webDriver).withTimeout(2, TimeUnit.SECONDS).pollingEvery(250, TimeUnit.MILLISECONDS);
            try {
                shortWait.until((WebDriver input) -> {
                    try {
                        input.findElement(By.id("quantity_wanted"));
                        return true;
                    } catch (NoSuchElementException e) {
                        return false;
                    }
                });
            } catch (TimeoutException e) {
                q--;
                continue;
            }
            wait.until(ExpectedConditions.elementToBeClickable(By.className("bootstrap-touchspin-up")));
            WebElement upButton = webDriver.findElement(By.className("bootstrap-touchspin-up"));
            for (int j = 1; j < quantities[q]; j++) {
                upButton.click();
            }
            wait.until(ExpectedConditions.elementToBeClickable(By.className("add-to-cart")));
            webDriver.findElement(By.className("add-to-cart")).click();
            try {
                Thread.sleep(Duration.ofSeconds(1));
            } catch (InterruptedException ex) {
            }
        }
        webDriver.navigate().refresh();
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("cart-products-count")));
        String result = webDriver.findElement(By.className("cart-products-count")).getText().replaceAll("[()]", "");
        assertEquals(((expectedResult + 1) * expectedResult) / 2, Integer.valueOf(result));
        return;
    }
    @Test
    public void testSearchAndAddToCart() {
        webDriver.get("http://localhost:8089/en/");
        webDriver.manage().timeouts().implicitlyWait(Duration.ofSeconds(5));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("ui-autocomplete-input")));
        WebElement searchBar = webDriver.findElement(By.className("ui-autocomplete-input"));
        searchBar.clear();
        //TODO change product name
        searchBar.sendKeys("cool");
        searchBar.sendKeys(Keys.ENTER);
        wait.until(ExpectedConditions.elementToBeClickable(By.className("product-thumbnail")));
        List<WebElement> productList = webDriver.findElements(By.className("product-thumbnail"));
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
        assertEquals(1, Integer.valueOf(result));
        return;
    }
    public void testRemoveFromCart() {

        return;
    }
}
