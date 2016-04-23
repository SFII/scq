var ResponseCard = React.createClass({

    getInitialState: function() {
        return({
            results: 0,
            iter: 0,
            length: 0
        })
    },

    componentDidMount: function() {
	if(test == false){
        $.ajax({
            url: "/api/results/" + this.props.surveyID,
            dataType: "json",
            type: 'GET',
            success: function(results){
                this.setState({results: results})
                this.setState({length: results.length})
                console.log(results)
            }.bind(this),
            error: function(xhr, status, err){
                console.error("/api/results", status, err.toString());
            }.bind(this)
        });
	}
	else{
	this.setState({
		results: [{ id: 123456, response_format: "multipleChoice", response_data: {series: [1,1,1], labels: ['option1','option2','option3']} }],
		length: 1
	});
	}
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
            <div className="responseCardDiv updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
            <TitleSection titleText={this.state.results[this.state.iter].title} />
            <ChartDiv 
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

var ChartDiv = React.createClass({
    
    getInitialState: function(){
        return{
            questionID: 0
        }
    },
    
    componentDidMount: function(){
        this.setState({
            questionID: this.props.questionID
        });
        this.updateChart(this.props.response_data.labels,this.props.response_data.series,this.props.question_format);
    },
    
    componentWillReceiveProps: function(nextProps){
        this.setState({
            questionID: nextProps.questionID
        });
        this.updateChart(nextProps.response_data.labels,nextProps.response_data.series,nextProps.question_format);
    },
    
    updateChart: function(labels,series,question_format,questionID){
	if(test == false){
        var chartCSS = "#chart" + this.state.questionID + "-chart";
        if(question_format == "rating"){    
            var data = {
                series: series,
                labels: labels
            };
            var options = {
                seriesBarDistance: 15
            };
            new Chartist.Bar(chartCSS,data,options)
        }
        else if(question_format == "multipleChoice"){
            var data={
                series: series,
                labels: labels
            };
            var options = {
                seriesBarDistance: 15
            };
            new Chartist.Bar(chartCSS,data,options)
        }
        else if(question_format == "trueOrFalse"){
            var data = {
                series: series,
                labels: labels
            };

            new Chartist.Pie(chartCSS,data);    
        }
	}
    },
    
    render: function(){
        var chartName = "chart" + this.state.questionID + "-chart";
        return(
	    <div className="chartDivDiv">
            <div className="ct-chart ct-golden-section" id={chartName}></div>
            </div>
        );
    }
});

var ResponseFooter = React.createClass({

    render:function(){

        if(this.props.currQuestion == 0 && this.props.numQuestions != 1){
            return(
                <div className="mdl-cell mdl-cell--12-col mdl-card__title mdl-card--expand mdl-300">
                    <button onClick={this.props.prevQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" disabled>
                            Previous
                    </button>
                    <Progress responseSize={this.props.currQuestion} numQuestions={this.props.numQuestions} />
                    <button onClick={this.props.nextQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
                            Next
                    </button>
                </div>
            );
        }

        else if(this.props.currQuestion > 0 && this.props.currQuestion < this.props.numQuestions - 1){
            return(
                <div className="mdl-cell mdl-cell--12-col mdl-card__title mdl-card--expand mdl-300">
                    <button onClick={this.props.prevQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
                            Previous
                    </button>
                    <Progress responseSize={this.props.currQuestion} numQuestions={this.props.numQuestions} />
                    <button onClick={this.props.nextQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
                            Next
                    </button>
                </div>
            );
        }
        else if(this.props.currQuestion == this.props.numQuestions - 1 && this.props.numQuestions != 1){
            return(
                <div className="mdl-cell mdl-cell--12-col mdl-card__title mdl-card--expand mdl-300">
                    <button onClick={this.props.prevQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
                            Previous
                    </button>
                    <Progress responseSize={this.props.currQuestion} numQuestions={this.props.numQuestions} />
                    <button onClick={this.props.nextQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" disabled>
                            Next
                    </button>
                </div>
            );
        }
        else if(this.props.numQuestions == 1){
            return(
                <div className="responseFooterDiv mdl-cell mdl-cell--12-col mdl-card__title mdl-card--expand mdl-300">
                    <button onClick={this.props.prevQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" disabled>
                            Previous
                    </button>
                    <Progress responseSize={this.props.currQuestion} numQuestions={this.props.numQuestions} />
                    <button onClick={this.props.nextQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent" disabled>
                            Next
                    </button>
                </div>
            );
        }
    }
});
