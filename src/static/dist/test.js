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

  render: function render() {
    return React.createElement(
      "div",
      { className: "updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop" },
      React.createElement(Card, { bullets: ['SAMPLE ONE', 'SAMPLE TWO', 'SAMPLE THREE'] })
    );
  }
});

var Goo = function Goo() {
  alert('hello');
  alert('ghasdhahjksd');
};

ReactDOM.render(React.createElement(Page, null), document.getElementById('main-grid'));