exports.config = {
    capabilities: {
        
        'browserName': 'chrome',
        'chromeOptions': {
            args: ['--disable-web-security']
        },
        shardTestFiles: true,
        maxInstances: 10
    },
    baseUrl: 'http://localhost:8100',
    specs: [
        './tests/e2e-tests/*.tests.js'
    ],
    jasmineNodeOpts: {
        isVerbose: true,
    }
};
