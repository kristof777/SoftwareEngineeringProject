// Karma configuration

module.exports = function (config) {
    config.set({

        // base path that will be used to resolve all patterns (eg. files, exclude)
        basePath: '',

        // frameworks to use
        // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
        frameworks: ['jasmine', 'karma-typescript'],

        // list of files / patterns to load in the browser
        files: [
            {pattern: "src/**/*.ts", include: true},
            {pattern: "node_modules/reflect-metadata/Reflect.js", include: true},
            {pattern: "tests/unit-tests/*.ts", include: true},

            {pattern: "src/pages/sign-in/sign-in.html", include: false, serve: true},
            {pattern: "src/app/app.html", include: false, serve: true},
            {pattern: "src/pages/sign-up/sign-up.html", include: false, serve: true},
            {pattern: "src/pages/add-listing/add-listing.html", include: false, serve: true},
            {pattern: "src/pages/edit-listings/edit-listings.html", include: false, serve: true},
            {pattern: "src/pages/favourites/favourites.html", include: false, serve: true},
            {pattern: "src/pages/filter/filter.html", include: false, serve: true},
            {pattern: "src/pages/change-password/change-password.html", include: false, serve: true},
            {pattern: "src/pages/main/main.html", include: false, serve: true},
            {pattern: "src/pages/my-listings/my-listings.html", include: false, serve: true},
            {pattern: "src/pages/settings/settings.html", include: false, serve: true},
            {pattern: "src/pages/browse/browse.html", include: false, serve: true},
        ],


        // list of files to exclude
        exclude: [],


        // preprocess matching files before serving them to the browser
        // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
        preprocessors: {
            '**/*.ts': ['karma-typescript'],
        },

        proxies: {
            '/sign-in.html': '/base/src/pages/sign-in/sign-in.html',
            '/app.html': '/base/src/app/app.html',
            '/sign-up.html': '/base/src/pages/sign-up/sign-up.html',
            '/add-listing.html': '/base/src/pages/add-listing/add-listing.html',
            '/edit-listings.html': '/base/src/pages/edit-listings/edit-listings.html',
            '/favourites.html': '/base/src/pages/favourites/favourites.html',
            '/filter.html': '/base/src/pages/filter/filter.html',
            '/change-password.html': '/base/src/pages/change-password/change-password.html',
            '/main.html': '/base/src/pages/main/main.html',
            '/my-listings.html': '/base/src/pages/my-listings/my-listings.html',
            '/settings.html': '/base/src/pages/settings/settings.html',
            '/browse.html': '/base/src/pages/browse/browse.html',
        },

        // test results reporter to use
        // possible values: 'dots', 'progress'
        // available reporters: https://npmjs.org/browse/keyword/karma-reporter
        reporters: ['progress', 'karma-typescript'],


        // web server port
        port: 9876,


        // enable / disable colors in the output (reporters and logs)
        colors: true,


        // level of logging
        // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
        logLevel: config.LOG_INFO,


        // enable / disable watching file and executing tests whenever any file changes
        autoWatch: true,


        // start these browsers
        // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
        browsers: ['Chrome'],

        // Continuous Integration mode
        // if true, Karma captures browsers, runs the tests and exits
        singleRun: true,

        // Concurrency level
        // how many browser should be started simultaneous
        concurrency: Infinity
    })
}
