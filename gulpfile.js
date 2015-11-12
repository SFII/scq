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
var cachebreaker = require('gulp-cache-breaker');


js_files = [
    './src/static/javascripts/db.js',
    './src/static/javascripts/base.js',
    './src/static/javascripts/cards.js',
    './src/static/javascripts/survey.js'
]

// Lint Task
gulp.task('lint', function() {
    return gulp.src('./src/static/javascripts/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

gulp.task('dev-js', function() {
    //these need to be sequential to prevent
    return gulp.src(js_files)
        .pipe(concat('all.js'))
        .pipe(babel())
        .pipe(rename('all.js'))
        .pipe(cachebreaker())
        .pipe(gulp.dest('./src/static/dist/'));
});

gulp.task('prod-js', function(){
    return gulp.src(js_files)
        .pipe(concat('all.js'))
        .pipe(babel())
        .pipe(gulp.dest('./dist/js/'))
        .pipe(rename('all.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('./src/static/dist/'));
})

gulp.task('minify-css', function () {
    gulp.src('./src/static/stylesheets/*.css')
        .pipe(minify({keepBreaks: true}))
        .pipe(rename({
            suffix: '.min.css'
        }))
        .pipe(gulp.dest('./src/static/dist/'));
});

// Watch Files For Changes
gulp.task('watch', function() {
    gulp.watch('./src/static/javascripts/*.js', ['lint', 'dev-js']);
});

// Default Task
gulp.task('default', ['scripts', 'minify-css']);
