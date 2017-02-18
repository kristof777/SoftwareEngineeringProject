exports.config = {
    capabilities: {
        //platformName: 'iOS',
        /*
        'browserName': 'chrome',
        'chromeOptions': {
            args: ['--disable-web-security']
        },
        */
        'browserName': 'firefox',
        SharedTestFiles: true,
    },
    baseUrl: 'http://localhost:8100',
    specs: [
        './tests/e2e-tests/*.tests.js'
    ],
    jasmineNodeOpts: {
        isVerbose: true,
    }
};

