/*
*
* Footer
* Just an mdl submit button, behaves as a normal submit button would
*/
var Footer = React.createClass({
    render: function() {
        if(this.props.questionNum == 0){
            return(
                <div className="mdl-grid mdl-card__title mdl-card--expand mdl-300">
                <button className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised" disabled>
                    Previous
                </button>

                <Progress
                questionNum = {this.props.questionNum}
                numQuestions = {this.props.numQuestions}
                responseSize={this.props.responseSize}/>

                <NextButton
                nextHandler={this.props.nextHandler}
                surveyData={this.props.surveyData}
                questionID={this.props.questionID}
                response_format={this.props.response_format}/>

                </div>
            );
        }
        else if(this.props.questionNum == this.props.numQuestions-1){
            return(
                <div className="mdl-grid mdl-card__title mdl-card--expand mdl-300">
                    <PrevButton
                    prevHandler={this.props.prevHandler}
                    surveyData={this.props.surveyData}
                    questionID={this.props.questionID}
                    response_format={this.props.response_format}/>

                    <Progress
                    questionNum = {this.props.questionNum}
                    numQuestions = {this.props.numQuestions}
                    responseSize={this.props.responseSize}/>

                    <SubmitButton
                    onSubmit={this.props.onSubmit}
                    surveyData={this.props.surveyData}
                    questionID={this.props.questionID}
                    response_format={this.props.response_format}/>
                </div>
            );
        }
        else{
        return(
       <div className="mdl-grid mdl-card__title mdl-card--expand mdl-300">

            <PrevButton
            prevHandler={this.props.prevHandler}
            surveyData={this.props.surveyData}
            questionID={this.props.questionID}
            response_format={this.props.response_format}/>

            <Progress
            questionNum = {this.props.questionNum}
            numQuestions = {this.props.numQuestions}
            responseSize={this.props.responseSize}/>

            <NextButton
            nextHandler={this.props.nextHandler}
            surveyData={this.props.surveyData}
            questionID={this.props.questionID}
            response_format={this.props.response_format}/>
        </div>
        );
        }
    }
})

/* I made an mdl progress bar, but it doesn't work well with React, so I'm only saving this in case we decide our current progress bar is ugly.
var Progress = React.createClass({
    
    getInitialState: function() {
    var progressValue = (this.props.responseSize/(this.props.numQuestions-1))*100;
    return({progressValue: progressValue})
    },
    
    componentDidUpdate: function() {
        console.log("update");
        document.querySelector('#myProgress').MaterialProgress.setProgress(this.state.progressValue);
    },
    
    render: function() {
        return (
        <div id="myProgress" className="mdl-cell mdl-cell--4-col mdl-progress mdl-js-progress"></div>
        )
    }
})
*/

var Progress = React.createClass({
    render: function() {
    var progressValue = (this.props.responseSize/(this.props.numQuestions-1))*100;
        return (
        <progress id="myProgress" className="mdl-cell mdl-cell--4-col bar" value={progressValue} max="100"></progress>
        )
    }
})

var PrevButton = React.createClass({
    clickHandler: function() {
        var surveyData = this.props.surveyData;
        var questionID = this.props.questionID;
        var response_format = this.props.response_format;
        this.props.prevHandler(surveyData,questionID,response_format);
    },
    render: function() {
        return (
        <button onClick={this.clickHandler} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
                Previous
            </button>
        )
    }
})

var NextButton = React.createClass({
    clickHandler: function() {
        var surveyData = this.props.surveyData;
        var questionID = this.props.questionID;
        var response_format = this.props.response_format;
        this.props.nextHandler(surveyData,questionID,response_format);
    },
    render: function() {
        return (
        <button onClick={this.clickHandler} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
                Next
        </button>
        )
    }
})

var SubmitButton = React.createClass({
    clickHandler:function(){
        var surveyData = this.props.surveyData;
        var questionID = this.props.questionID;
        var response_format = this.props.response_format;
        this.props.onSubmit(surveyData, questionID, response_format);
    },
    render: function(){
        return(
        <button onClick={this.clickHandler} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-color--accent">
                Submit
        </button>
        )
    }
})