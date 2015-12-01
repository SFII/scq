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
* Submit Button
*/
"use strict";

var SubmitButton = React.createClass({
    displayName: "SubmitButton",

    render: function render() {
        return React.createElement(
            "button",
            { className: "mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect" },
            "Submit"
        );
    }
});

/*
*
* Multiple Choice
*/
var MultipleChoice = React.createClass({
    displayName: "MultipleChoice",

    render: function render() {
        var renderedOptions = this.props.options.map(function (option) {
            return React.createElement(
                "div",
                null,
                React.createElement(
                    "label",
                    { className: "mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect" },
                    React.createElement("input", { type: "checkbox", key: option, className: "mdl-checkbox__input" }),
                    React.createElement(
                        "span",
                        { className: "mdl-checkbox__label" },
                        " ",
                        option,
                        " ",
                        React.createElement("br", null)
                    )
                )
            );
        });

        return React.createElement(
            "div",
            { className: "mdl-card__supporting-text mdl-color-text--grey-600" },
            renderedOptions,
            React.createElement(SubmitButton, null)
        );
    }
});
/*
*
*
* Single Choice
*/
var SingleChoice = React.createClass({
    displayName: "SingleChoice",

    render: function render() {
        var renderedOptions = this.props.options.map(function (option, type) {
            return React.createElement(
                "div",
                null,
                React.createElement(
                    "label",
                    { className: "mdl-radio mdl-js-radio mdl-js-ripple-effect" },
                    React.createElement("input", { type: "radio", className: "mdl-radio__button", name: option, value: option, key: option }),
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
            { className: "mdl-card__supporting-text mdl-color-text--grey-600" },
            React.createElement(
                "form",
                { className: "mdl-card__supporting-text mdl-color-text--grey-600" },
                renderedOptions,
                React.createElement(SubmitButton, null)
            )
        );
    }
});
/*
*
*
* Free
*/
var FreeResponse = React.createClass({
    displayName: "FreeResponse",

    render: function render() {
        return React.createElement(
            "div",
            { className: "mdl-card__supporting-text mdl-color-text--grey-600" },
            React.createElement("textarea", { className: "mdl-textfield__input", type: "text", rows: "4", cols: "110", id: "test" }),
            React.createElement("br", null),
            React.createElement(SubmitButton, null)
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

var Card = React.createClass({
  displayName: "Card",

  render: function render() {
    if (this.props.type == "multipeChoice") {
      return React.createElement(
        "div",
        { className: "updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop" },
        React.createElement(
          "div",
          null,
          React.createElement(TitleSection, { titleText: this.props.title }),
          React.createElement(MultipleChoice, { options: this.props.options })
        )
      );
    } else if (this.props.type == "trueOrFalse") {
      return React.createElement(
        "div",
        { className: "updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop" },
        React.createElement(
          "div",
          null,
          React.createElement(TitleSection, { titleText: this.props.title }),
          React.createElement(SingleChoice, { options: this.props.options })
        )
      );
    } else if (this.props.type == "freeResponse") {
      return React.createElement(
        "div",
        { className: "updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop" },
        React.createElement(
          "div",
          null,
          React.createElement(TitleSection, { titleText: this.props.title }),
          React.createElement(FreeResponse, null)
        )
      );
    } else {
      alert("not Valid card type");
      return undefined;;
    }
  }
});
"use strict";

var testQuestions = [{
    id: 1,
    type: "trueOrFalse",
    title: "Would you recommend this course?",
    options: ["Yes", "No"]
}, {
    id: "asdasdad",
    type: "freeResponse",
    title: "What things should be improved?"
}, {
    id: 2,
    type: "multipeChoice",
    title: "Did you enjoy the course?",
    options: ["Not at all", "It was an average course", "It was an excellent course"]
}];

/*
*
* MainDiv
*ask michael about this.props.class
*/
var MainDiv = React.createClass({
    displayName: "MainDiv",

    render: function render() {
        var itemNodes = testQuestions.map(function (item) {
            return React.createElement(Card, { title: item.title, options: item.options, type: item.type });
        });
        return React.createElement(
            "div",
            { className: "mainDiv " },
            itemNodes
        );
    }
});

var Page = React.createClass({
    displayName: "Page",

    render: function render() {
        return React.createElement(
            "div",
            { className: "mdl-grid mdl-cell--12-col content" },
            React.createElement(MainDiv, { question: this.props.question })
        );
    }
});

/*
*
* Form
*
*/
var Form = React.createClass({
    displayName: "Form",

    addItem: function addItem(e) {
        e.preventDefault();
        this.props.onItemSubmit({});
        return;
    },

    render: function render() {
        return React.createElement(
            "form",
            { className: "listForm", onSubmit: this.addItem },
            React.createElement("input", { type: "submit", value: "Click me" })
        );
    }
});