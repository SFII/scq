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
                <div>
                    <MediumCard survey={getSurvey('PUT ENDPOINT HERE')}>
                    </MediumCard>
                </div>
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