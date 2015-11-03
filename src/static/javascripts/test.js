var Title = React.createClass({
  render: function(){
    return (
      <div className="mdl-card__title mdl-card--expand mdl-color--teal-300">
        <h2 className="mdl-card__title-text"> { this.props.titleText } </h2>
      </div>
    );
  }
});

var Support = React.createClass({
  propTypes: {
    bullets: React.PropTypes.array.isRequired
  },

  render: function(){
    const bulletPoints = this.props.bullets.map((bullet) => {
      return <li key={ bullet }>{ bullet }</li>;
    });

    return (
      <div className="mdl-card__supporting-text mdl-color-text--grey-600">
        <ul className="mdl-card__supporting-text mdl-color-text--grey-600">
          { bulletPoints }
        </ul>
      </div>
    );
  }
});

var Card = React.createClass({
  propTypes: {
      bullets: React.PropTypes.array.isRequired
  },

  render: function(){
    return (
      <div>
        <Title titleText="Updates!" />
        <Support bullets={ this.props.bullets }/>
      </div>
    );
  }
});

var Page = React.createClass({
  render: function(){
    return (
      <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
        <Card bullets={ ['SAMPLE ONE', 'SAMPLE TWO', 'SAMPLE THREE'] }/>
      </div>);
  }
});

var Goo = function(){
    alert('hello')
}

ReactDOM.render(<Page/>, document.getElementById('main-grid'));