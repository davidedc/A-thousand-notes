// example:
// node download-via-puppeteer.js "https://www.youtube.com/watch?v=DjeN1Ea8uns&feature=share"

const puppeteer = require('puppeteer');


var theArgs = process.argv.slice(2);


(async () => {
  const browser = await puppeteer.launch({args: ['--no-sandbox', '--disable-setuid-sandbox']});
  const page = await browser.newPage();
  await page.goto(theArgs[0]);
  await page.screenshot({path: 'buddy-screenshot.png'});

  await browser.close();
})();