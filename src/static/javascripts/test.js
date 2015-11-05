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

    handleAddItem: function(){

        //taken current state
        var newItem = this.state.data;

        var addItem = newItem.concat([" "]);
        this.setState({data: addItem});
    },

    getInitialState: function() {
        return {data: []};
    },

    render: function(){
      return (

        <div className="mdl-grid mdl-cell--12-col content">
        <Form onItemSubmit={this.handleAddItem}/>

        <MainDiv data={this.state.data}/>


        <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">

          <Card bullets={ ['SAMPLE ONE', 'SAMPLE TWO', 'SAMPLE THREE'] }/>


        </div>
        </div>
        );
    }
  });

var BigCard = React.createClass({
    render: function() {
        return (
            <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
            <Card bullets={ ['SAMPLE ONE', 'SAMPLE TWO', 'SAMPLE THREE'] }/>
        </div>

        );
    }
});


/*
*
* MainDiv
*ask michael about this.props.class
*/
var MainDiv = React.createClass({
    render: function() {
        var itemNodes = this.props.data.map(function (item) {
                return (
                    <BigCard>
                    </BigCard>
                );
            });
        return (
        <div className="mainDiv ">
            {itemNodes}
        </div>
        );
    }
});

/*
*
* Form
*
*/
var Form = React.createClass({

    addItem: function(e) {
        e.preventDefault();
        this.props.onItemSubmit({});
        return;

    },

    render: function() {
        return (
        <form className="listForm" onSubmit={this.addItem}>
        <input  type="submit" value="Click me" />
        </form>
        );
    }
});

ReactDOM.render(<Page /> , document.getElementById('main-grid'));
