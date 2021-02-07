// example:
// node note-from-opengraph.js "https://www.youtube.com/watch?v=DjeN1Ea8uns&feature=share"

const ogs = require('open-graph-scraper');

var theArgs = process.argv.slice(2);

const options = {
  url: theArgs[0],
  customMetaTags: [{
    multiple: false, // is there more then one of these tags on a page (normally this is false)
    property: 'hostname', // meta tag name/property attribute
    fieldName: 'hostnameMetaTag', // name of the result variable
  }],
};
ogs(options)
  .then((data) => {
    const { error, result, response } = data;
    console.log('hostnameMetaTag:', result); // hostnameMetaTag: github.com
  })