var ResponseCard = React.createClass({

    getInitialState: function() {
        return({
            results: 0,
            iter: 0
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
    if(this.state.results != 0){
        return(
            <div className="updates mdl-card">
            <QuestionDiv 
            questionID={this.state.results[this.state.iter].id} 
            question_format={this.state.results[this.state.iter].response_format} 
            response_data={this.state.results[this.state.iter].response_data}/>
            </div>
            
        );
    }
    else{
        return(
        <div></div>
        );
    }
    },
});

var QuestionDiv = React.createClass({

    componentDidMount: function(){
            var chartCSS = "#chart" + this.props.questionID + "-chart";
            if(this.props.question_format == "rating"){    
                var data = {
                    series: this.props.response_data.series,
                    labels: this.props.response_data.labels
                };
                var options = {
                    seriesBarDistance: 15
                };
                new Chartist.Bar(chartCSS,data,options)
            }
            else if(this.props.question_format == "multipleChoice"){
                var data={
                    series: this.props.response_data.series,
                    labels: this.props.response_data.labels
                };
                var options = {
                    seriesBarDistance: 15
                };
                new Chartist.Bar(chartCSS,data,options)
            }
            else if(this.props.question_format == "trueOrFalse"){
                var data = {
                    series: this.props.response_data.series,
                    labels: this.props.response_data.labels
                };

                new Chartist.Pie(chartCSS,data);    
            }
    },
    
    render: function(){
        var chartName = "chart" + this.props.questionID + "-chart";
        return(
            <div className="ct-chart ct-golden-section" id={chartName}></div>
        );
    }
});