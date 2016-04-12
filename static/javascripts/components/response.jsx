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
                this.setState({results: results})
                console.log(this.state.results);
            }.bind(this),
            error: function(xhr, status, err){
                console.error("/api/results", status, err.toString());
            }.bind(this)
        });
    },

    render: function(){
    //map each object in results array to a div, we need different charts d
    //depending on the question type
    console.log(Object.prototype.toString.call(this.state.results));
    var questionNodes = this.state.results.map(function(item) {
        if(item.response_format == "rating"){
            var data = {
                series : item.bar_data.series,
                labels : item.bar_data.labels
            };
            var options= {
                seriesBarDistance: 15
            };
            new Chartist.Bar('.chart',data, options)
        }
        //pie data is represented as the set of options chosen with a value indicating
        //how many times that set is chosen.
        else if(item.response_format == "trueOrFalse"){

        }
        else if(item.response_format == "multipleChoice"){

        }
        else if(item.response_format == "freeResponse"){

        }

    });
    
    
        return(
            <div className="updates chart mdl-card">
            </div>
        );
    },
});
