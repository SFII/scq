// Include gulp
var gulp = require('gulp');

// Include Our Plugins
var jshint = require('gulp-jshint');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var minify = require('gulp-minify-css');
var babel = require('gulp-babel');

// Lint Task
gulp.task('lint', function() {
    return gulp.src('./assets/javascripts/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

// Concatenate & Minify JS
gulp.task('scripts', function() {
    return gulp.src('./assets/javascripts/*.js')
        .pipe(concat('all.js'))
        .pipe(babel())
        .pipe(gulp.dest('dist/js/'))
        .pipe(rename('all.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('dist/js/'));
});

gulp.task('minify-css', function () {
    gulp.src('./assets/stylesheets/*.css')
        .pipe(minify({keepBreaks: true}))
        .pipe(rename({
            suffix: '.min.css'
        }))
        .pipe(gulp.dest('dist/css/'))
    ;
});

// Watch Files For Changes
gulp.task('watch', function() {
    gulp.watch('./assets/javascripts/*.js', ['lint', 'scripts']);
});

// Default Task
gulp.task('default', ['lint', 'scripts', 'minify-css','watch']);
