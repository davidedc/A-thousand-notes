// Example:
//   node download-via-puppeteer-2.js "https://twitter.com/ntsutae/status/1367089088315068419" > inspect-tweet-markdown.md
// or
//   node download-via-puppeteer-2.js "https://twitter.com/ntsutae/status/1367089088315068419" | pandoc -f markdown_strict -t html | pandoc -f html --extract-media ./assets/thefilename  -t markdown_strict -o thefilename.md
//
// To install gifify
//   https://github.com/vvo/gifify

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






  const tweetHTML = element_property.toString();
  //console.log(tweetHTML);
  const URLsRegexp = /(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])/igm;

  let m;
  var theVideoURLs = []

  while ((m = URLsRegexp.exec(tweetHTML)) !== null) {
      // This is necessary to avoid infinite loops with zero-width matches
      if (m.index === URLsRegexp.lastIndex) {
          URLsRegexp.lastIndex++;
      }

      var results = m.filter(theURL => theURL.includes(".mp4"));
      
      // The result can be accessed through the `m`-variable.
      results.forEach((match) => {
          console.log(match);
          theVideoURLs.push(match);
      });
  }


  var { execSync } = require('child_process');
  // stderr is sent to stdout of parent process
  // you can set options.stdio if you want it to go elsewhere


  theVideoURLs.forEach((URLwithVideo) => {

      var reg = /\/([^\/]*)\.mp4/ig;
      var match;
      var videoIDs = [];

      while (match = reg.exec(URLwithVideo)) {
        videoIDs.push(match[1] || match[0]);
      }

      console.log("video id: " + videoIDs);

      var command = 'youtube-dl ' + URLwithVideo
      console.log(command);
      var stdout = execSync(command);

      var command = 'gifify  ' + videoIDs + "-" + videoIDs + ".mp4 -o " + videoIDs + ".gif"
      console.log(command);
      var stdout = execSync(command);

      var command = 'mkdir  ./assets/thefilename/'
      console.log(command);
      var stdout = execSync(command);

      var command = 'mv  ' + videoIDs + ".gif ./assets/thefilename/"
      console.log(command);
      var stdout = execSync(command);

      pageContentMarkdown = pageContentMarkdown + "\n\n![](assets/thefilename/"+ videoIDs + ".gif)"

  });



  //console.log(element_property.toString().replaceAll("JSHandle:", "").replaceAll("<svg", "<!--").replaceAll("/svg>", "-->").replaceAll("Copy link to Tweet","").replaceAll("<div", "\n\n<div"))
  //console.log(element_property.toString())

  // just some tests on how to embed/download a video is needed
  console.log(pageContentMarkdown);

  buffer = await insideFrame.screenshot(options);

  await browser.close();

})();