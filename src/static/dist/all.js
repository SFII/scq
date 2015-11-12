"use strict";

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
            React.createElement(MainDiv, { data: this.state.data })
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
            return React.createElement(
                "div",
                null,
                React.createElement(MediumCard, { survey: getSurvey('PUT ENDPOINT HERE') })
            );
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
var Card = React.createClass({
    displayName: "Card",

    propTypes: {
        survey: React.PropTypes.object.isRequired
    },

    render: function render() {
        return React.createElement(
            "div",
            null,
            React.createElement(TitleSection, { titleText: "Updates!" }),
            React.createElement(SupportSection, { survey: this.props.survey })
        );
    }
});

var MediumCard = React.createClass({
    displayName: "MediumCard",

    propTypes: {
        survey: React.PropTypes.object.isRequired
    },

    render: function render() {
        return React.createElement(
            "div",
            { className: "updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--8-col" },
            React.createElement(Card, { survey: this.props.survey })
        );
    }
});

var SmallCard = React.createClass({
    displayName: "SmallCard",

    render: function render() {
        return React.createElement(
            "div",
            { className: "updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col" },
            React.createElement(Card, { bullets: ['Small', 'TEST', 'SAMPLE THREE'] })
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

var SupportSection = React.createClass({
    displayName: "SupportSection",

    render: function render() {
        return React.createElement(
            "div",
            { className: "mdl-card__supporting-text mdl-color-text--grey-600" },
            this.props.survey
        );
    }
});

var Table = React.createClass({
    displayName: "Table",

    render: function render() {
        return React.createElement(
            "table",
            { className: "mdl-js-data-table mdl-data-table--selectable" },
            React.createElement(
                "thead",
                null,
                React.createElement(
                    "tr",
                    null,
                    React.createElement(
                        "th",
                        { className: "mdl-data-table__cell--non-numeric" },
                        "Material"
                    ),
                    React.createElement(
                        "th",
                        null,
                        "Quantity"
                    ),
                    React.createElement(
                        "th",
                        null,
                        "Unit price"
                    )
                )
            ),
            React.createElement(
                "tbody",
                null,
                React.createElement(
                    "tr",
                    null,
                    React.createElement(
                        "td",
                        { className: "mdl-data-table__cell--non-numeric" },
                        "Acrylic (Transparent)"
                    ),
                    React.createElement(
                        "td",
                        null,
                        "250"
                    ),
                    React.createElement(
                        "td",
                        null,
                        "$2.90"
                    )
                ),
                React.createElement(
                    "tr",
                    null,
                    React.createElement(
                        "td",
                        { className: "mdl-data-table__cell--non-numeric" },
                        "Plywood (Birch)"
                    ),
                    React.createElement(
                        "td",
                        null,
                        "50"
                    ),
                    React.createElement(
                        "td",
                        null,
                        "$1.25"
                    )
                ),
                React.createElement(
                    "tr",
                    null,
                    React.createElement(
                        "td",
                        { className: "mdl-data-table__cell--non-numeric" },
                        "Laminate (Gold on Blue)"
                    ),
                    React.createElement(
                        "td",
                        null,
                        "10"
                    ),
                    React.createElement(
                        "td",
                        null,
                        "$12.35"
                    )
                )
            )
        );
    }
});