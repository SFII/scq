"use strict";

var Title = React.createClass({
    displayName: "Title",

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

var Support = React.createClass({
    displayName: "Support",

    propTypes: {
        bullets: React.PropTypes.array.isRequired
    },

    render: function render() {
        var bulletPoints = this.props.bullets.map(function (bullet) {
            return React.createElement(
                "li",
                { key: bullet },
                bullet
            );
        });

        return React.createElement(
            "div",
            { className: "mdl-card__supporting-text mdl-color-text--grey-600" },
            React.createElement(
                "ul",
                { className: "mdl-card__supporting-text mdl-color-text--grey-600" },
                bulletPoints
            )
        );
    }
});

var Card = React.createClass({
    displayName: "Card",

    propTypes: {
        bullets: React.PropTypes.array.isRequired
    },

    render: function render() {
        return React.createElement(
            "div",
            null,
            React.createElement(Title, { titleText: "Updates!" }),
            React.createElement(Support, { bullets: this.props.bullets })
        );
    }
});

var Page = React.createClass({
    displayName: "Page",

    handleAddItem: function handleAddItem() {

        //taken current state
        var newItem = this.state.data;

        var addItem = newItem.concat([" "]);
        this.setState({ data: addItem });
    },

    getInitialState: function getInitialState() {
        return { data: [] };
    },

    render: function render() {
        return React.createElement(
            "div",
            { className: "mdl-grid mdl-cell--12-col content" },
            React.createElement(Form, { onItemSubmit: this.handleAddItem }),
            React.createElement(MainDiv, { data: this.state.data }),
            React.createElement(
                "div",
                { className: "updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop" },
                React.createElement(Card, { bullets: ['SAMPLE ONE', 'SAMPLE TWO', 'SAMPLE THREE'] })
            )
        );
    }
});

var BigCard = React.createClass({
    displayName: "BigCard",

    render: function render() {
        return React.createElement(
            "div",
            { className: "updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop" },
            React.createElement(Card, { bullets: ['SAMPLE ONE', 'SAMPLE TWO', 'SAMPLE THREE'] })
        );
    }
});

/*
*
* MainDiv
*ask michael about this.props.class
*/
var MainDiv = React.createClass({
    displayName: "MainDiv",

    render: function render() {
        var itemNodes = this.props.data.map(function (item) {
            return React.createElement(BigCard, null);
        });
        return React.createElement(
            "div",
            { className: "mainDiv " },
            itemNodes
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

ReactDOM.render(React.createElement(Page, null), document.getElementById('main-grid'));