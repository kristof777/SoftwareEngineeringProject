exports.config = {
    onPrepare: function(){
        let SpecReporter = require('jasmine-spec-reporter').SpecReporter;
        jasmine.getEnv().addReporter(new SpecReporter({displayStacktrace: 'all'}));
    },

    capabilities: {
        'browserName': 'firefox',
        shardTestFiles: true,
        maxInstances: 10
    },
    baseUrl: 'http://localhost:8100',
    specs: [
        //'./tests/e2e-tests/*.tests.js'
        './tests/e2e-tests/regression.tests.js'
    ],
    jasmineNodeOpts: {
        isVerbose: true,
    }
};

