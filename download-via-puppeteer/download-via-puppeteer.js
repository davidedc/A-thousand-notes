// Example:
// node download-via-puppeteer.js "https://twitter.com/ntsutae/status/1367089088315068419"

const puppeteer = require('puppeteer');

var theArgs = process.argv.slice(2);


(async () => {

  const browser = await puppeteer.launch({args: ['--no-sandbox', '--disable-setuid-sandbox']});

  const options = { encoding: "base64", fullPage: false , path: 'buddy-screenshot.png'};
  const page = await browser.newPage();
  let buffer;

    await page.setViewport({
      width: 767,
      height: 800,
      deviceScaleFactor: 2,
    });
    const tUrl = `https://publish.twitter.com/?query=${theArgs[0]}&widget=Tweet`;
    await page.goto(tUrl, { waitUntil: "networkidle2" });
    await page.waitFor(3000);
    await page.evaluate((sel) => {
      const elem = document.querySelector(sel);
      elem.parentNode.removeChild(elem);
    }, "body #top");
    const selector = "body #WidgetConfigurator-preview .twitter-tweet";
    await page.waitForSelector(selector); // wait for the selector to load
    const element = await page.$(selector); // declare a variable with an ElementHandle
    buffer = await element.screenshot(options);
  await browser.close();


})();



