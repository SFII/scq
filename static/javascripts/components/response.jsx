var ResponseCard = React.createClass({

    getInitialState: function() {
        return({results: []})
    },

    componentDidMount: function() {
        $.ajax({
            url: "/api/results/" + this.props.surveyID,
            dataType: "json",
            type: 'GET',
            success: function(results){
                console.log(results) //TODO for debugging, remove me.
                this.setState({results: results})
            }.bind(this),
            error: function(xhr, status, err){
                console.error("/api/results", status, err.toString());
            }.bind(this)
        });
    },

    render: function(){
        return(
            <div className="updates mdl-card">
                {JSON.stringify(this.state.results)}
            </div>
        );
    },
});
