exports.config = {
    onPrepare: function(){
        let SpecReporter = require('jasmine-spec-reporter').SpecReporter;
        jasmine.getEnv().addReporter(new SpecReporter({displayStacktrace: 'all'}));
    },
    capabilities: {
        //platformName: 'iOS',
        'browserName': 'chrome',
        'chromeOptions': {
            args: ['--disable-web-security']
        }
        //'browserName': 'firefox',
    },
    baseUrl: 'http://localhost:8100',
    specs: [
        'registerBrowseAddListing.tests.js'
    ],
    jasmineNodeOpts: {
        isVerbose: true,
    }
};
