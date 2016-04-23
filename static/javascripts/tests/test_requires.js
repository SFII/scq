var React = require('react'),
    assert = require('assert'),
    TestUtils = require('react-addons-test-utils'),
    jsdom = require('jsdom');

global.document = jsdom.jsdom('<!doctype html><html><body></body></html>');
global.window = document.parentWindow;

var test = true

var data = [{
"closed_timestamp" : null,
"created_timestamp" : 1461290509.1686077,
"creator_id": "e8bd8109-e631-40a8-bc8b-12333277f89d",
"creator_name" : "brau7176",
"deleted" : false,
"id" : "bc1cf800-d8ad-41b9-9e10-abe5886badb9",
"item_id" : "Test Group",
"item_name" : "Test Title",
"item_type" : "Group",
"questions" : [{
	"id" : "c0ea9fed-21b8-4280-8deb-37e198632bb1",
	"options" : ["A","B","C","D"],
	"response_format" : "multipleChoice",
	"title" : "Test Question"	
	}],
"responses" : []
}]

var user_data = [{
    "accepted_tos": true ,
    "answered_surveys": [ ],
    "answers": [ ],
    "created_surveys": [
        "bc1cf800-d8ad-41b9-9e10-abe5886badb9"
    ] ,
    "date_registered": 1461290415.5090678 ,
    "departments": [
        "Library administration"
    ] ,
    "dob": "06/23/1994" ,
    "email": "brady.auen@colorado.edu",
    "ethnicity": "White" ,
    "gender": "Male" ,
    "id": "e8bd8109-e631-40a8-bc8b-12333277f89d" ,
    "last_sign_in": 1461290415.5090995 ,
    "majors": [
        "Computer science"
    ] ,
    "minors": [ ],
    "native_language": "English" ,
    "pending_groups": [ "TestPendingGroup" ],
    "primary_affiliation": "Student" ,
    "registration": "registration_culdap" ,
    "status": "Senior" ,
    "subscribed_groups": [
        "TestSubscribedGroup"
    ] ,
    "survey_responses": [ ],
    "unanswered_surveys": [
        "bc1cf800-d8ad-41b9-9e10-abe5886badb9"
    ] ,
    "username": "brau7176"
}]

var extra_data = [{
'gender': ['Male', 'Female', 'Other', 'Prefer Not to Disclose'],
'primary_affiliation': ['Student', 'Faculty', 'Both'],
'ethnicity': ['American Indian or Alaska Native', 'Asian', 'Black or African American', 'Hispanic or Latino', 'Native Hawaiian or Other Pacific Islander', 'White', 'Other', 'Prefer Not to Disclose'],
'native_language': ['English', 'Spanish', 'French', 'German', 'Korean', 'Chinese', 'Japanese', 'Russian', 'Arabic', 'Portuguese', 'Hindi', 'Other', 'Prefer Not to Disclose'],
'status': ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate', 'Ph.D']
}]

