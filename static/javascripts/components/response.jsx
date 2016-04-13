var ResponseCard = React.createClass({

    getInitialState: function() {
        return({
            results: []
        })
    },

    componentDidMount: function() {
        $.ajax({
            url: "/api/results/" + this.props.surveyID,
            dataType: "json",
            type: 'GET',
            success: function(results){
                this.setState({results: results})
                console.log(this.state.results);
            }.bind(this),
            error: function(xhr, status, err){
                console.error("/api/results", status, err.toString());
            }.bind(this)
        });
    },

    render: function(){
    var questionNodes = this.state.results.map(function(item) {
    if(item.response_format == "rating"){
        var data = {
            series: item.bar_data.series,
            labels: item.bar_data.labels
        };
        var options = {
            seriesBarDistance: 15
        };
        new Chartist.Bar('.chart',data,options)
    }
    });
        return(
            <div className="updates chart mdl-card">
            </div>
        );
    },
});