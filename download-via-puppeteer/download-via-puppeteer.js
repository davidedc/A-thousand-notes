// Example:
//   node download-via-puppeteer.js "https://twitter.com/ntsutae/status/1367089088315068419"
// or
//   node download-via-puppeteer.js "https://twitter.com/ntsutae/status/1367089088315068419" | pandoc -f html --extract-media ./assets/thefilename  -t markdown_strict  -o thefilename.md

const puppeteer = require('puppeteer');

var theArgs = process.argv.slice(2);

(async () => {

  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--disable-web-security',
      '--disable-features=IsolateOrigins,site-per-process'
    ]
  });

  const options = {
    fullPage: false,
    path: 'buddy-screenshot.png'
  };
  const page = await browser.newPage();
  let buffer;

  await page.setViewport({
    width: 767,
    height: 800,
    deviceScaleFactor: 2,
  });

  const tUrl = `https://publish.twitter.com/?query=${theArgs[0]}&widget=Tweet`;
  await page.goto(tUrl, {
    waitUntil: "networkidle2"
  });

  await page.evaluate((sel) => {
    const elem = document.querySelector(sel);
    elem.parentNode.removeChild(elem);
  }, "body #top");

  const selector = "body #WidgetConfigurator-preview .twitter-tweet";
  await page.waitForSelector(selector); // wait for the selector to load

  const pageBody = await page.$(selector);
  var element_property = await pageBody.getProperty('innerHTML');
  //console.log("pageBody: " + element_property)

  var iFrameSelector = "iframe[id='twitter-widget-0']"
  const frameHandle = await pageBody.$(iFrameSelector);
  //console.log("frameHandle?: " + frameHandle)

  const frameHandleAsElement = await frameHandle.asElement();
  //console.dir("frameHandleAsElement?: " + frameHandle)

  element_property = await pageBody.getProperty('innerHTML');
  //console.log("frame?: " + element_property)

  //await frameHandle.evaluate(node => console.log("frameHandle evaluate: " + node.innerText))

  const frame = await frameHandle.contentFrame();
  await frame.waitForSelector("span"); // wait for the selector to load

  const insideFrame = await frame.$('body #app article');

  element_property = await insideFrame.getProperty('innerHTML');
  console.log(element_property.toString().replaceAll("JSHandle:", "").replaceAll("<svg", "<!--").replaceAll("/svg>", "-->").replaceAll("Copy link to Tweet","").replaceAll("<div", "\n\n<div"))
  //console.log(element_property.toString())

  buffer = await insideFrame.screenshot(options);

  await browser.close();

})();