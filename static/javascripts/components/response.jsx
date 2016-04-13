var ResponseCard = React.createClass({

    getInitialState: function() {
        return({
            results: [7],
            iter: 3
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
                console.log(this.state.results[this.state.iter]);
            }.bind(this),
            error: function(xhr, status, err){
                console.error("/api/results", status, err.toString());
            }.bind(this)
        });
    },

    render: function(){
    if(this.state.results[this.state.iter] != null){
        return(
            <div className="updates mdl-card">
            <QuestionCard question={this.state.results[this.state.iter]} />
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

var QuestionCard = React.createClass({

    render:function(){
        if(this.props.question.response_format == "rating"){
            var data = {
                series : this.props.question.bar_data.series,
                labels : this.props.question.bar_data.labels
            };
            var options= {
                seriesBarDistance: 15
            };
            new Chartist.Bar('.chart',data, options)
        }
        //pie data is represented as the set of options chosen with a value indicating
        //how many times that set is chosen.
        else if(this.props.question.response_format == "trueOrFalse"){

        }
        else if(this.props.question.response_format == "multipleChoice"){

        }
        else if(this.props.question.response_format == "freeResponse"){

        }
        
        return(
        <div className="chart">
        </div>
        );
    }
});