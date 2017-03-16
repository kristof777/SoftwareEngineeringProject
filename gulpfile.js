var gulp = require('gulp');
var preprocess = require('gulp-preprocess');
var destination = './src/app/';
var destination_file = './src/app/kasper-config.ts';
var source = './kasper-config.ts';
var del = require('del');


gulp.task('delete', function () {
    del.sync(destination_file);
});

gulp.task('test', ['delete'], function () {
    gulp.src(source)
        .pipe(preprocess({context: {NODE_ENV: 'TEST'}}))
        .pipe(gulp.dest(destination));
});


gulp.task('dev', ['delete'], function () {
    gulp.src(source)
        .pipe(preprocess({context: {NODE_ENV: 'DEV'}}))
        .pipe(gulp.dest(destination));
});

gulp.task('default', function () {
    console.log("Please use either gulp test or gulp env");
});
