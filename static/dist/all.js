'use strict';

function getSurvey(url) {
    $.ajax({
        url: url,
        type: 'GET',
        async: false,
        cache: false,
        timeout: 30000,
        error: function error() {
            return {};
        },
        success: function success(data) {
            console.log(data);
            return data;
        }
    });
}

function sendSurvey(url) {}
/*
*
* Footer
* Just an mdl submit button, behaves as a normal submit button would
*/
"use strict";

var Footer = React.createClass({
    displayName: "Footer",

    render: function render() {
        if (this.props.questionNum == 0) {
            return React.createElement(
                "div",
                { className: "mdl-grid mdl-card__title mdl-card--expand mdl-300" },
                React.createElement(
                    "button",
                    { className: "mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised", disabled: true },
                    "Previous"
                ),
                React.createElement(Progress, {
                    questionNum: this.props.questionNum,
                    numQuestions: this.props.numQuestions,
                    responseSize: this.props.responseSize }),
                React.createElement(NextButton, {
                    nextHandler: this.props.nextHandler,
                    surveyData: this.props.surveyData,
                    questionID: this.props.questionID,
                    response_format: this.props.response_format })
            );
        } else if (this.props.questionNum == this.props.numQuestions - 1) {
            return React.createElement(
                "div",
                { className: "mdl-grid mdl-card__title mdl-card--expand mdl-300" },
                React.createElement(PrevButton, {
                    prevHandler: this.props.prevHandler,
                    surveyData: this.props.surveyData,
                    questionID: this.props.questionID,
                    response_format: this.props.response_format }),
                React.createElement(Progress, {
                    questionNum: this.props.questionNum,
                    numQuestions: this.props.numQuestions,
                    responseSize: this.props.responseSize }),
                React.createElement(SubmitButton, {
                    onSubmit: this.props.onSubmit,
                    surveyData: this.props.surveyData,
                    questionID: this.props.questionID,
                    response_format: this.props.response_format })
            );
        } else {
            return React.createElement(
                "div",
                { className: "mdl-grid mdl-card__title mdl-card--expand mdl-300" },
                React.createElement(PrevButton, {
                    prevHandler: this.props.prevHandler,
                    surveyData: this.props.surveyData,
                    questionID: this.props.questionID,
                    response_format: this.props.response_format }),
                React.createElement(Progress, {
                    questionNum: this.props.questionNum,
                    numQuestions: this.props.numQuestions,
                    responseSize: this.props.responseSize }),
                React.createElement(NextButton, {
                    nextHandler: this.props.nextHandler,
                    surveyData: this.props.surveyData,
                    questionID: this.props.questionID,
                    response_format: this.props.response_format })
            );
        }
    }
});

/* I made an mdl progress bar, but it doesn't work well with React, so I'm only saving this in case we decide our current progress bar is ugly.
var Progress = React.createClass({
    
    getInitialState: function() {
    var progressValue = (this.props.responseSize/(this.props.numQuestions-1))*100;
    return({progressValue: progressValue})
    },
    
    componentDidUpdate: function() {
        console.log("update");
        document.querySelector('#myProgress').MaterialProgress.setProgress(this.state.progressValue);
    },
    
    render: function() {
        return (
        <div id="myProgress" className="mdl-cell mdl-cell--4-col mdl-progress mdl-js-progress"></div>
        )
    }
})
*/

var Progress = React.createClass({
    displayName: "Progress",

    render: function render() {
        var progressValue = this.props.responseSize / (this.props.numQuestions - 1) * 100;
        return React.createElement("progress", { id: "myProgress", className: "mdl-cell mdl-cell--4-col bar", value: progressValue, max: "100" });
    }
});

var PrevButton = React.createClass({
    displayName: "PrevButton",

    clickHandler: function clickHandler() {
        var surveyData = this.props.surveyData;
        var questionID = this.props.questionID;
        var response_format = this.props.response_format;
        this.props.prevHandler(surveyData, questionID, response_format);
    },
    render: function render() {
        return React.createElement(
            "button",
            { onClick: this.clickHandler, className: "mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" },
            "Previous"
        );
    }
});

var NextButton = React.createClass({
    displayName: "NextButton",

    clickHandler: function clickHandler() {
        var surveyData = this.props.surveyData;
        var questionID = this.props.questionID;
        var response_format = this.props.response_format;
        this.props.nextHandler(surveyData, questionID, response_format);
    },
    render: function render() {
        return React.createElement(
            "button",
            { onClick: this.clickHandler, className: "mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" },
            "Next"
        );
    }
});

var SubmitButton = React.createClass({
    displayName: "SubmitButton",

    clickHandler: function clickHandler() {
        var surveyData = this.props.surveyData;
        var questionID = this.props.questionID;
        var response_format = this.props.response_format;
        this.props.onSubmit(surveyData, questionID, response_format);
    },
    render: function render() {
        return React.createElement(
            "button",
            { onClick: this.clickHandler, className: "mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-color--purple" },
            "Submit"
        );
    }
});

/*
*
* Multiple Choice
* All the cards are very similar so I'm not going to copy and paste
*/
var MultipleChoice = React.createClass({
    displayName: "MultipleChoice",

    getInitialState: function getInitialState() {
        var length = Object.keys(this.props.options).length;
        var questionObj = [];
        for (var i = 0; i < length; i++) {
            questionObj[i] = false;
        }
        return { data: questionObj };
    },

    handleChange: function handleChange(i, value) {
        var NewValue = null;
        if (value == false) {
            NewValue = true;
        } else {
            NewValue = false;
        }
        var changeAnswer = this.state.data;
        changeAnswer[i] = NewValue;
        this.setState({ data: changeAnswer });
    },

    render: function render() {
        var _this = this;

        var renderedOptions = this.props.options.map(function (option, i) {
            return React.createElement(
                "label",
                { className: "mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect" },
                React.createElement("input", {
                    type: "checkbox",
                    value: _this.state.data[i],
                    name: option,
                    key: i,
                    className: "mdl-checkbox__input",
                    onChange: _this.handleChange.bind(_this, i, _this.state.data[i]) }),
                React.createElement(
                    "span",
                    { className: "mdl-checkbox__label" },
                    " ",
                    option,
                    " "
                )
            );
        });
        return React.createElement(
            "div",
            { className: "options mdl-card__supporting-text mdl-color-text--grey-600" },
            renderedOptions,
            React.createElement(Footer, {
                prevHandler: this.props.prevHandler,
                nextHandler: this.props.nextHandler,
                onSubmit: this.props.onSubmit,
                surveyData: this.state.data,
                questionID: this.props.questionID,
                response_format: this.props.response_format,
                questionNum: this.props.questionNum,
                numQuestions: this.props.numQuestions,
                responseSize: this.props.responseSize })
        );
    }
});
/*
*
*
* Single Choice
* This is the same as multiple choice, but the handlers are different
* so that once a new option is chosen all other options are set to false
* since it simulates a radio form
*/
var SingleChoice = React.createClass({
    displayName: "SingleChoice",

    getInitialState: function getInitialState() {
        var length = Object.keys(this.props.options).length;
        var questionObj = [];
        for (var i = 0; i < length; i++) {
            questionObj[i] = false;
        }
        return { data: questionObj };
    },

    handleChange: function handleChange(i, value) {
        var NewValue = null;
        var length = Object.keys(this.props.options).length;
        var questionObj = [];
        var changeAnswer = this.state.data;
        for (var iter = 0; iter < length; iter++) {
            changeAnswer[iter] = false;
        }
        changeAnswer[i] = true;
        this.setState({ data: changeAnswer });
    },

    render: function render() {
        var _this2 = this;

        var surveyID = String(this.props.surveyID);
        var renderedOptions = this.props.options.map(function (option, i) {
            return React.createElement(
                "div",
                null,
                React.createElement(
                    "label",
                    { className: "mdl-radio mdl-js-radio mdl-js-ripple-effect" },
                    React.createElement("input", {
                        type: "radio",
                        className: "mdl-radio__button",
                        name: surveyID,
                        value: i,
                        onChange: _this2.handleChange.bind(_this2, i, _this2.state.data[i]) }),
                    React.createElement(
                        "span",
                        { className: "mdl-radio__label" },
                        " ",
                        option,
                        " "
                    )
                )
            );
        });

        return React.createElement(
            "div",
            {
                className: "mdl-card__supporting-text mdl-color-text--grey-600" },
            renderedOptions,
            React.createElement(Footer, {
                prevHandler: this.props.prevHandler,
                nextHandler: this.props.nextHandler,
                onSubmit: this.props.onSubmit,
                surveyData: this.state.data,
                questionID: this.props.questionID,
                response_format: this.props.response_format,
                questionNum: this.props.questionNum,
                numQuestions: this.props.numQuestions,
                responseSize: this.props.responseSize })
        );
    }
});
/*
*
*
* Free
* Same as the other cards, but simpler, we just take whatever is in the
* textfield and get it to POST
*/
var FreeResponse = React.createClass({
    displayName: "FreeResponse",

    getInitialState: function getInitialState() {
        return { answer: 'Change Me' };
    },

    handleChange: function handleChange(e) {
        this.setState({ answer: e.target.value });
    },

    render: function render() {
        return React.createElement(
            "div",
            {
                className: "mdl-card__supporting-text mdl-color-text--grey-600" },
            React.createElement("textarea", {
                className: "mdl-textfield__input",
                type: "text",
                rows: "4",
                id: "test",
                value: this.state.answer,
                onChange: this.handleChange }),
            React.createElement("br", null),
            React.createElement(Footer, {
                prevHandler: this.props.prevHandler,
                nextHandler: this.props.nextHandler,
                onSubmit: this.props.onSubmit,
                surveyData: this.state.answer,
                questionID: this.props.questionID,
                response_format: this.props.response_format,
                questionNum: this.props.questionNum,
                numQuestions: this.props.numQuestions,
                responseSize: this.props.responseSize })
        );
    }
});
/*
*Rating slider
*This still needs work from Michael and I
*/
var Rating = React.createClass({
    displayName: "Rating",

    getInitialState: function getInitialState() {
        return { answer: 5 };
    },

    handleChange: function handleChange(e) {
        this.setState({ answer: e.target.value });
    },
    render: function render() {
        return React.createElement(
            "div",
            { className: "mdl-card__supporting-text mdl-color-text--grey-600" },
            React.createElement(
                "div",
                null,
                React.createElement("input", { className: "mdl-slider mdl-js-slider",
                    type: "range",
                    min: "0",
                    max: "10",
                    value: this.state.answer,
                    step: "1",
                    onChange: this.handleChange
                }),
                React.createElement(
                    "span",
                    { id: "sliderStatus" },
                    this.state.answer
                )
            ),
            React.createElement(Footer, {
                prevHandler: this.props.prevHandler,
                nextHandler: this.props.nextHandler,
                onSubmit: this.props.onSubmit,
                surveyData: this.state.answer,
                questionID: this.props.questionID,
                response_format: this.props.response_format,
                questionNum: this.props.questionNum,
                numQuestions: this.props.numQuestions,
                responseSize: this.props.responseSize })
        );
    }
});
"use strict";

var TitleSection = React.createClass({
  displayName: "TitleSection",

  render: function render() {
    return React.createElement(
      "div",
      { className: "mdl-card__title mdl-card--expand mdl-color--teal-300" },
      React.createElement(
        "h2",
        { className: "mdl-card__title-text" },
        " ",
        this.props.titleText,
        " "
      )
    );
  }
});
//Card is really messy
var Card = React.createClass({
  displayName: "Card",

  /* an initial state called response, actually not entirely sure
   * why we have it.. :)
  */
  getInitialState: function getInitialState() {
    return { response: [] };
  },
  componentDidUpdate: function componentDidUpdate() {
    componentHandler.upgradeDom();
  },

  //handleSurveySubmit is called whenever a submit button is pushed
  //it calls POST on /api/response sending a JSON of the survey data
  //and on success calls the removeHandler which removes the
  //corresponding cards
  //case matching of the question type, generates the corresponding
  //card, eventually we want one card per survey, this will be tricky
  render: function render() {
    if (this.props.response_format == "multipleChoice") {
      return React.createElement(
        "div",
        { className: "updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop" },
        React.createElement(
          "div",
          null,
          React.createElement(TitleSection, { titleText: this.props.title }),
          React.createElement(MultipleChoice, {
            options: this.props.options,
            onSubmit: this.props.onSubmit,
            nextHandler: this.props.nextHandler,
            prevHandler: this.props.prevHandler,
            surveyID: this.props.surveyID,
            department: this.props.department,
            creator: this.props.creator,
            isInstructor: this.props.isInstructor,
            questionID: this.props.questionID,
            response_format: this.props.response_format,
            questionNum: this.props.questionNum,
            numQuestions: this.props.numQuestions,
            responseSize: this.props.responseSize })
        )
      );
    } else if (this.props.response_format == "rating") {
      return React.createElement(
        "div",
        { className: "updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop" },
        React.createElement(
          "div",
          null,
          React.createElement(TitleSection, { titleText: this.props.title }),
          React.createElement(Rating, {
            surveyID: this.props.surveyID,
            department: this.props.department,
            creator: this.props.creator,
            isInstructor: this.props.isInstructor,
            onSubmit: this.props.onSubmit,
            nextHandler: this.props.nextHandler,
            prevHandler: this.props.prevHandler,
            surveyID: this.props.surveyID,
            questionID: this.props.questionID,
            response_format: this.props.response_format,
            questionNum: this.props.questionNum,
            numQuestions: this.props.numQuestions,
            responseSize: this.props.responseSize })
        )
      );
    } else if (this.props.response_format == "trueOrFalse") {
      return React.createElement(
        "div",
        { className: "updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop" },
        React.createElement(
          "div",
          null,
          React.createElement(TitleSection, { titleText: this.props.title }),
          React.createElement(SingleChoice, {
            options: this.props.options,
            onSubmit: this.props.onSubmit,
            nextHandler: this.props.nextHandler,
            prevHandler: this.props.prevHandler,
            surveyID: this.props.surveyID,
            department: this.props.department,
            creator: this.props.creator,
            isInstructor: this.props.isInstructor,
            questionID: this.props.questionID,
            response_format: this.props.response_format,
            questionNum: this.props.questionNum,
            numQuestions: this.props.numQuestions,
            responseSize: this.props.responseSize })
        )
      );
    } else if (this.props.response_format == "freeResponse") {
      return React.createElement(
        "div",
        { className: "updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop" },
        React.createElement(
          "div",
          null,
          React.createElement(TitleSection, { titleText: this.props.title }),
          React.createElement(FreeResponse, {
            onSubmit: this.props.onSubmit,
            nextHandler: this.props.nextHandler,
            prevHandler: this.props.prevHandler,
            surveyID: this.props.surveyID,
            department: this.props.department,
            creator: this.props.creator,
            isInstructor: this.props.isInstructor,
            questionID: this.props.questionID,
            response_format: this.props.response_format,
            questionNum: this.props.questionNum,
            numQuestions: this.props.numQuestions,
            responseSize: this.props.responseSize })
        )
      );
    } else {
      alert("not Valid card type");
      return undefined;;
    }
  }
});
/*
* Page is the overall container that gets mounted into our HTML file
*/
"use strict";

var Page = React.createClass({
    displayName: "Page",

    /*
    //loadPageJSON is the function we call whenever we want to call GET on the surveys endpoint
        loadPageJSON: function() {
        $.ajax({
        url: this.props.routes.surveys,
        type: 'GET',
        dataType: 'json',
        cache: true,
        success: function(data){
        //on success we set the state of Page to be equal to the JSON received
        this.setState({data: data});
        }.bind(this),
        error: function(xhr, status, err){
            console.error(this.props.routes.surveys, status, err.toString());
        }.bind(this)
        });
        },
        //This is where the initial loadPageJSON call happens, it happens when the React class is instantiated (Carlos we should put that
        //initial fetch Sam showed you here)
        getInitialState: function() {
        //this.loadPageJSON();
            return{data:[]};
        },
    
        //This is something we'll likely want to change, it calls loadPageJSON again once the component mounts, which doesn't really make sense, oops
    
        //MainDiv is sent the data state as "pageJson" and the api routes json as "routes"
        */

    render: function render() {
        return React.createElement(
            "div",
            { className: "mdl-grid mdl-cell--12-col content" },
            React.createElement(MainDiv, /*pageJson={this.state.data}*/{ routes: this.props.routes })
        );
    }
});

/*
*
* MainDiv
* At this layer we separate each Survey into separate SurveyDiv objects
*/
var MainDiv = React.createClass({
    displayName: "MainDiv",

    render: function render() {
        if (!loggedIn()) {
            return React.createElement(Welcome, null);
        }
        routesObject = this.props.routes;
        //itemNodes is the set of mapped items (each one is a survey) and each is passed it's set of questions, routes, and other relevant information
        /*this is set to testQuestions.map until the GET works, if it's
        working switch it to this.props.pageJson and it should work */
        var itemNodes = data.map(function (item) {
            return React.createElement(SurveyDiv, {
                key: item.id,
                questions: item.questions,
                routes: routesObject,
                surveyID: item.id,
                department: item.department,
                creator: item.creator,
                isInstructor: item.isInstructor });
        });
        return React.createElement(
            "div",
            { className: "mainDiv " },
            itemNodes,
            React.createElement(SurveyCreationCard, null)
        );
    }
});

var SurveyDiv = React.createClass({
    displayName: "SurveyDiv",

    //We want our Survey cards to disappear once submitted, so the getInitialState and removeCard functions provide a boolean
    //that we check before/while rendering

    getInitialState: function getInitialState() {
        return {
            length: Object.keys(this.props.questions).length,
            showCard: true,
            iter: 0,
            responseSize: 0,
            response: {
                survey_id: this.props.surveyID,
                question_responses: []
            }
        };
    },

    handleSurveySubmit: function handleSurveySubmit(survey, questionID, response_format) {
        var response = this.state.response;
        var question_responses_object = {
            response_format: response_format,
            question_id: questionID,
            response_data: survey
        };

        var length = Object.keys(response.question_responses).length;
        for (var i = length - 1; i >= 0; i--) {
            if (response.question_responses[i].question_id == questionID) {
                response.question_responses.splice(i, 1);
            }
        }
        response.question_responses.push(question_responses_object);
        this.setState({ response: response });

        $.ajax({
            url: this.props.routes.response,
            contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify(response),
            success: (function (data) {
                console.log(response);
                this.removeCard();
            }).bind(this),
            error: (function (xhr, status, err) {
                console.log(this.state.response);
                console.error("/api/response", status, err.toString());
            }).bind(this)
        });
    },

    removeCard: function removeCard() {
        this.setState({ showCard: false });
    },

    nextQuestion: function nextQuestion(survey, questionID, response_format) {
        var response = this.state.response;
        var question_responses_object = {
            response_format: response_format,
            question_id: questionID,
            response_data: survey
        };

        var length = Object.keys(response.question_responses).length;
        for (var i = length - 1; i >= 0; i--) {
            if (response.question_responses[i].question_id == questionID) {
                response.question_responses.splice(i, 1);
            }
        }

        response.question_responses.push(question_responses_object);

        this.setState({ response: response });
        this.setState({ responseSize: Object.keys(this.state.response.question_responses).length });

        var iter = this.state.iter;
        if (iter == this.state.length - 1) {
            this.handleSurveySubmit(this.state.response);
        } else {
            this.setState({ iter: iter + 1 });
        }
    },

    prevQuestion: function prevQuestion(survey, questionID, response_format) {
        var response = this.state.response;
        var question_responses_object = {
            response_format: response_format,
            question_id: questionID,
            response_data: survey
        };

        var length = Object.keys(response.question_responses).length;
        for (var i = length - 1; i >= 0; i--) {
            if (response.question_responses[i].question_id == questionID) {
                response.question_responses.splice(i, 1);
            }
        }

        response.question_responses.push(question_responses_object);

        this.setState({ response: response });
        this.setState({ responseSize: Object.keys(this.state.response.question_responses).length });

        var iter = this.state.iter;

        this.setState({ iter: iter - 1 });
    },

    render: function render() {
        //increasing the scope of the props, there has to be a better way to do this.
        //if showCard state is true, then we map the surveys questions onto cards, else we map nothing, pass all properties again.
        if (this.state.showCard == true) {
            return React.createElement(
                "div",
                { className: "surveyDiv" },
                React.createElement(Card, {
                    routes: this.props.routes,
                    questionNum: this.state.iter,
                    questionID: this.props.questions[this.state.iter].id,
                    responseSize: this.state.responseSize,
                    numQuestions: this.state.length,
                    title: this.props.questions[this.state.iter].title,
                    options: this.props.questions[this.state.iter].options,
                    response_format: this.props.questions[this.state.iter].response_format,
                    surveyID: this.props.surveyID,
                    department: this.props.department,
                    creator: this.props.creator,
                    isInstructor: this.props.isInstructor,
                    removeHandler: this.removeCard,
                    nextHandler: this.nextQuestion,
                    prevHandler: this.prevQuestion,
                    onSubmit: this.handleSurveySubmit })
            );
        } else {
            return React.createElement("div", null);
        }
    }
});

function loggedIn() {
    return document.cookie.indexOf("user") > -1;
}
"use strict";

var Welcome = React.createClass({
	displayName: "Welcome",

	render: function render() {
		return React.createElement(
			"div",
			null,
			React.createElement(About, null),
			React.createElement(Login, null)
		);
	}
});

var About = React.createClass({
	displayName: "About",

	render: function render() {
		return React.createElement(
			"div",
			{ className: "updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--8-col" },
			React.createElement(
				"p",
				null,
				"Campus Consensus is a survey and data collection system developed for improving student-faculty relationships at universities being developed at University Colorado at Boulder. Our platform allows students and faculty to ask questions and offer short surveys to improve instructional quality, align student and faculty interests, and express consensus about campus issues."
			),
			React.createElement(
				"p",
				null,
				"Students in the same class or department can learn about how other students feel about the quality of the course or what is working and what is not. Similarly, faculty can get fine-grain information about how their instruction is being received by their students."
			),
			React.createElement(
				"p",
				null,
				"Our data will be available to the entire campus in an anonymous form. The project is being developed by computer science seniors at University of Colorado Boulder."
			),
			React.createElement(
				"p",
				null,
				"Please contact our project leads with any questions:"
			),
			React.createElement(
				"ul",
				null,
				React.createElement(
					"li",
					null,
					"antsankov [at] gmail [dot] com"
				),
				React.createElement(
					"li",
					null,
					"michael [dot] skirpan [at] colorado [dot] edu"
				)
			)
		);
	}
});

var Login = React.createClass({
	displayName: "Login",

	render: function render() {
		return React.createElement(
			"div",
			{ className: "updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col" },
			React.createElement(
				"form",
				{ action: "/register/culdap", method: "post" },
				React.createElement(
					"label",
					null,
					"CU Login Name"
				),
				React.createElement("input", { type: "text", name: "username", required: true }),
				React.createElement(
					"label",
					null,
					"Password"
				),
				React.createElement("input", { type: "password", name: "password", required: true }),
				React.createElement("input", { type: "submit", id: "loginbtn", name: "login", value: "Log In", "class": "button" })
			)
		);
	}
});
/*
* Page with the Card for the creation of surveys
*/

"use strict";

var SurveyCreationCard = React.createClass({
    displayName: "SurveyCreationCard",

    render: function render() {
        return React.createElement(
            "div",
            { className: "updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop" },
            React.createElement(
                "div",
                null,
                React.createElement(TitleSection, { titleText: "Create a Survey" }),
                React.createElement(Fields, null)
            )
        );
    }
});

var Fields = React.createClass({
    displayName: "Fields",

    //set initial value
    getInitialState: function getInitialState() {
        return { value: 'select' };
    },

    //set value change
    changeHandler: function changeHandler(event) {
        this.setState({ value: event.target.value });
    },

    render: function render() {
        return React.createElement(
            "div",
            { className: "mdl-card__supporting-text mdl-color-text--grey-600" },
            React.createElement(
                "h4",
                null,
                "Add a Question:"
            ),
            React.createElement(
                "form",
                null,
                React.createElement(
                    "p",
                    null,
                    "Title:",
                    React.createElement("input", { type: "text", name: "title_question" })
                ),
                React.createElement(
                    "p",
                    null,
                    "Type:",
                    React.createElement(
                        "select",
                        { id: "mySelect", onChange: this.changeHandler, value: this.state.value },
                        React.createElement(
                            "option",
                            { disabled: true, value: "select" },
                            " Select an option "
                        ),
                        React.createElement(
                            "option",
                            { value: "multipleChoice" },
                            "Multiple Choice"
                        ),
                        React.createElement(
                            "option",
                            { value: "singleChoice" },
                            "Single Choice"
                        ),
                        React.createElement(
                            "option",
                            { value: "rating" },
                            "Rating"
                        ),
                        React.createElement(
                            "option",
                            { value: "freeResponse" },
                            "Open Response"
                        )
                    )
                )
            ),
            React.createElement(Question, { value: this.state.value })
        );
    }
});

var Question = React.createClass({
    displayName: "Question",

    //mdl in new questions
    componentDidUpdate: function componentDidUpdate() {
        componentHandler.upgradeDom();
    },

    changeHandler: function changeHandler(event) {
        //not sure if needed
        this.setState({ value: event.target.value });
    },

    //render different options for multiple & single choice
    /*
    *
    render: function(){
      const options = this.props.options.map((option) => {
        return (
          <li className="mdl-list__item">
            <input  type="text"  placeholder="Introduce an option" onChange={this.changeHandler}/>
          </li>
        )
      });
    *
    */

    render: function render() {

        if (this.props.value == "multipleChoice") {
            return React.createElement(
                "div",
                null,
                React.createElement(
                    "ul",
                    { className: "mdl-list" },
                    options
                ),
                React.createElement(
                    "ul",
                    { className: "no_bullets mdl-list" },
                    React.createElement(
                        "li",
                        { className: "mdl-list__item" },
                        React.createElement(
                            "p",
                            null,
                            React.createElement(
                                "button",
                                { className: "mdl-button mdl-js-button mdl-button--fab mdl-button--mini-fab" },
                                React.createElement(
                                    "i",
                                    { className: "material-icons" },
                                    "add"
                                )
                            ),
                            "    ADD QUESTION"
                        )
                    )
                )
            );
        } else if (this.props.value == "singleChoice") {
            return React.createElement("input", { type: "text", value: this.props.value, onChange: this.changeHandler });
        } else if (this.props.value == "rating") {
            return React.createElement("input", { type: "text", value: this.props.value, onChange: this.changeHandler });
        } else if (this.props.value == "freeResponse") {
            return React.createElement("input", { type: "text", value: this.props.value, onChange: this.changeHandler });
        } else {
            return React.createElement("p", { onChange: this.changeHandler });
        }
    }
});
"use strict";

/*
* Page with the card with the sample survey
*/