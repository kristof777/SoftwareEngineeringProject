exports.config = {
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
        'filterScreen.js'
    ],
    jasmineNodeOpts: {
        isVerbose: true,
    }
};
