var ResponseCard = React.createClass({

    getInitialState: function() {
        return({
            results: 0,
            iter: 0,
            length: 0
        })
    },

    componentDidMount: function() {
        $.ajax({
            url: "/api/results/" + this.props.surveyID,
            dataType: "json",
            type: 'GET',
            success: function(results){
                this.setState({results: results})
                this.setState({length: results.length})
            }.bind(this),
            error: function(xhr, status, err){
                console.error("/api/results", status, err.toString());
            }.bind(this)
        });
    },
    
    nextQuestion: function() {
        var iter = this.state.iter;
        
        this.setState({
            iter: iter + 1
        });
    },
    
    prevQuestion: function() {
        var iter = this.state.iter;
        
        this.setState({
            iter: iter - 1
        });
    },

    render: function(){
    if(this.state.results != 0){
        return(
            <div className="updates mdl-card">
            <QuestionDiv 
            questionID={this.state.results[this.state.iter].id} 
            question_format={this.state.results[this.state.iter].response_format} 
            response_data={this.state.results[this.state.iter].response_data} />
            
            <ResponseFooter 
            nextQuestion={this.nextQuestion}
            prevQuestion={this.prevQuestion}
            currQuestion={this.state.iter}
            numQuestions={this.state.length} />
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
        this.updateChart();
    },
    
    componentWillReceiveProps: function(){
        this.updateChart();
    },
    
    updateChart: function(){
        console.log(this.props.questionID)
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

var ResponseFooter = React.createClass({

    render:function(){

        if(this.props.currQuestion == 0 && this.props.numQuestions != 1){
            return(
                <div>
                    <button onClick={this.props.prevQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" disabled>
                            Previous
                    </button>

                    <button onClick={this.props.nextQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
                            Next
                    </button>
                </div>
            );
        }

        else if(this.props.currQuestion > 0 && this.props.currQuestion < this.props.numQuestions - 1){
            return(
                <div>
                        <button onClick={this.props.prevQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
                                Previous
                        </button>

                        <button onClick={this.props.nextQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
                                Next
                        </button>
                </div>
            );
        }
        else if(this.props.currQuestion == this.props.numQuestions - 1 && this.props.numQuestions != 1){
            return(
                <div>
                        <button onClick={this.props.prevQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
                                Previous
                        </button>

                        <button onClick={this.props.nextQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" disabled>
                                Next
                        </button>
                </div>
            );
        }
        else if(this.props.numQuestions == 1){
            return(
                <div>

                        <button onClick={this.props.prevQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" disabled>
                                Previous
                        </button>

                        <button onClick={this.props.nextQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" disabled>
                                Next
                        </button>
                </div>
            );
        }
    }

});