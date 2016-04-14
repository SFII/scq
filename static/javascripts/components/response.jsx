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
            series: item.response_data.series,
            labels: item.response_data.labels
        };
        var options = {
            seriesBarDistance: 15
        };
        new Chartist.Bar('.chart1',data,options)
    }
    else if(item.response_format == "multipleChoice"){
        var data={
            series: [item.response_data.series],
            labels: item.response_data.labels
        };
        var options = {
            seriesBarDistance: 15
        };
        new Chartist.Bar('.chart2',data,options)
    }
    else if(item.response_format == "trueOrFalse"){
        var data = {
          series: item.response_data.series,
          labels: item.response_data.labels
        };

        new Chartist.Pie('.chart3', data);    
    }
    });
        return(
            <div className="updates mdl-card">
            <div className="chart1"></div>
            <div className="chart2"></div>
            <div className="chart3"></div>
            </div>
            
        );
    },
});