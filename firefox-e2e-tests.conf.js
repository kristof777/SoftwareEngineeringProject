exports.config = {
    onPrepare: function(){
        let SpecReporter = require('jasmine-spec-reporter').SpecReporter;
        jasmine.getEnv().addReporter(new SpecReporter({displayStacktrace: 'all'}));
    },

    capabilities: {
        'browserName': 'firefox',
        shardTestFiles: true,
        maxInstances: 3
    },
    baseUrl: 'http://localhost:8100',
    specs: [
        './tests/e2e-tests/*.tests.js'
    ],
    exclude: [
        './tests/e2e-tests/registerUser.tests.js'
    ],
    jasmineNodeOpts: {
        isVerbose: true,
    }
};

