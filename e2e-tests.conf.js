exports.config = {
    capabilities: {
        /*
        'browserName': 'chrome',
        'chromeOptions': {
            args: ['--disable-web-security']
        },
        */
        'browserName': 'firefox',
        shardTestFiles: true,
    },
    baseUrl: 'http://localhost:8100',
    specs: [
        './tests/e2e-tests/ryans.tests.js',
        './tests/e2e-tests/filterScreen.tests.js'
    ],
    jasmineNodeOpts: {
        isVerbose: true,
    }
};

