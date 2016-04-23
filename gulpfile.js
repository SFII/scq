// Include gulp
var gulp = require('gulp');

// Include Our Plugins
var jshint = require('gulp-jshint');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var minify = require('gulp-minify-css');
var gulpBabel = require('gulp-babel');
var plumber = require('gulp-plumber');
var mocha = require('gulp-mocha');
var babel = require('babel-core/register');


js_files = [
    './static/javascripts/db.js',
    './static/javascripts/components/notTesting.jsx',
    './static/javascripts/components/questions.jsx',
    './static/javascripts/components/cards.jsx',
    './static/javascripts/components/dashboard.jsx',
    './static/javascripts/components/welcome.jsx',
    './static/javascripts/components/survey_card.jsx',
    './static/javascripts/components/survey_sample.jsx',
    './static/javascripts/components/footer.jsx',
    './static/javascripts/components/profile.jsx',
    './static/javascripts/components/profile_groups.jsx',
    './static/javascripts/components/groups_page.jsx',
    './static/javascripts/components/search_card.jsx',
    './static/javascripts/components/response.jsx',
    './static/javascripts/components/help.jsx'
]

test_js_files_1 = [
    './static/javascripts/db.js',
    './static/javascripts/components/questions.jsx',
    './static/javascripts/components/cards.jsx',
    './static/javascripts/components/dashboard.jsx',
    './static/javascripts/components/welcome.jsx',
    './static/javascripts/components/survey_card.jsx',
    './static/javascripts/components/survey_sample.jsx',
    './static/javascripts/components/footer.jsx',
    './static/javascripts/components/profile.jsx',
    './static/javascripts/components/profile_groups.jsx',
    './static/javascripts/components/groups_page.jsx',
    './static/javascripts/components/search_card.jsx',
    './static/javascripts/components/response.jsx',
    './static/javascripts/components/help.jsx'
]

test_js_files_2 = [
    './static/javascripts/tests/test_requires.js',
    './static/dist/all.js',
    './static/javascripts/tests/test-content.js' 
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
        .pipe(gulpBabel())
        .pipe(concat('all.js'))
        .pipe(rename('all.js'))
        .pipe(gulp.dest('./static/dist/'));
});

gulp.task('prod-js', function(){
    return gulp.src(js_files)
        .pipe(gulpBabel())
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

gulp.task('test-compile-1',function(cb) {
	return gulp.src(test_js_files_1)
	    .pipe(gulpBabel())
	    .pipe(concat('all.js'))
	    .pipe(gulp.dest('./static/dist/'))
	cb();
})

gulp.task('test-compile-2', ['test-compile-1'], function(cb) {
	return gulp.src(test_js_files_2)    
	    .pipe(concat('test.js'))
	    .pipe(gulp.dest('./test/'));
	cb();	
})

gulp.task('test-run', ['test-compile-2'], function () {
	gulp.src('./test/test.js')	
	.pipe(mocha({
           reporter: 'spec',
	   compilers: {
	     js:babel
	   }
        }))
});

// Default Task
gulp.task('default', ['scripts', 'minify-css']);
