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
                    <Table>
                    </Table>
                    <SmallCard>
                    </SmallCard>
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