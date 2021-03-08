// Example:
//   node download-via-puppeteer-2.js "https://twitter.com/ntsutae/status/1367089088315068419" > inspect-tewet-markdown.md
// or
//   node download-via-puppeteer-2.js "https://twitter.com/ntsutae/status/1367089088315068419" | pandoc -f markdown_strict -t html | pandoc -f html --extract-media ./assets/thefilename  -t markdown_strict  -o thefilename.md

const puppeteer = require('puppeteer');
const TurndownService = require('turndown');

const turndownService = new TurndownService();
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

  element_property_string = element_property.toString().replaceAll("JSHandle:", "");
  element_property_string = element_property_string.replaceAll("<svg", "<!--").replaceAll("/svg>", "-->");
  element_property_string = element_property_string.replaceAll("Copy link to Tweet","").replaceAll("<div", "\n\n<div");
  element_property_string = element_property_string.replaceAll("<div", "\n\n<div");


  pageContentMarkdown = turndownService.turndown(element_property_string);

  // take away all empty links i.e. the privacy link:
  // [](https://help.twitter.com/en/twitter-for-websites-ads-info-and-privacy)
  pageContentMarkdown = pageContentMarkdown.replaceAll(/[^!]\[\s*\]\([^\)]*\)/g,"");

  
  // remove some odd spacing in the links created by turndown
  // because they confuse pandoc
  pageContentMarkdown = pageContentMarkdown.replaceAll(/\[\n+/gm,"[");
  pageContentMarkdown = pageContentMarkdown.replaceAll(/\n+\]/gm,"]");
  pageContentMarkdown = pageContentMarkdown.replaceAll(/\n*(@[^\]]*]\(http)/gm," $1");

  // remove the first line since it's a link to the tweet *embed card*, which is a fairly mangled URL
  pageContentMarkdown = pageContentMarkdown.replaceAll(/^\[\s*\]\([^\)]*\)/gm,"");


  // just some tests on how to embed/download a video is needed
  //pageContentMarkdown = pageContentMarkdown + "\n\n![also the video](https://video.twimg.com/ext_tw_video/1367088823839064066/pu/vid/960x630/fkWREbwmsHUjN62t.mp4)"



  console.log(pageContentMarkdown)
  //console.log(element_property.toString());


  //console.log(element_property.toString().replaceAll("JSHandle:", "").replaceAll("<svg", "<!--").replaceAll("/svg>", "-->").replaceAll("Copy link to Tweet","").replaceAll("<div", "\n\n<div"))
  //console.log(element_property.toString())

  buffer = await insideFrame.screenshot(options);

  await browser.close();

})();