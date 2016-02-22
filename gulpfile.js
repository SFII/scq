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
var plumber = require('gulp-plumber');


js_files = [
    './static/javascripts/db.js',
    './static/javascripts/components/questions.jsx',
    './static/javascripts/components/cards.jsx',
    './static/javascripts/components/dashboard.jsx',
    './static/javascripts/components/welcome.jsx',
    './static/javascripts/components/survey_card.jsx',
    './static/javascripts/components/survey_sample.jsx',
    './static/javascripts/components/footer.jsx'

]

// Lint Task
gulp.task('lint', function() {
    return gulp.src(js_files)
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

gulp.task('dev-js', function() {
    //these need to be sequential to prevent
    return gulp.src(js_files)
        .pipe(plumber({
			errorHandler: function(err) {
				console.log(err);
				this.emit('end');
			}
		}))
        .pipe(babel())
        .pipe(concat('all.js'))
        .pipe(rename('all.js'))
        .pipe(gulp.dest('./static/dist/'));
});

gulp.task('prod-js', function(){
    return gulp.src(js_files)
        .pipe(babel())
        .pipe(concat('all.js'))
        .pipe(gulp.dest('./static/dist/'))
        .pipe(rename('all.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('./static/dist/'));
})

gulp.task('minify-css', function () {
    gulp.src('./static/stylesheets/*.css')
        .pipe(minify({keepBreaks: true}))
        .pipe(rename({
            suffix: '.min.css'
        }))
        .pipe(gulp.dest('./static/dist/'));
});

// Watch Files For Changes
gulp.task('watch', function() {
    gulp.watch(js_files, ['dev-js']);

});

// Default Task
gulp.task('default', ['scripts', 'minify-css']);
