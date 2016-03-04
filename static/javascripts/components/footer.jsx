/*
*
* Footer
* Contains a combination of Next, Previous, and Submit buttons either active or inactive when they're inapplicable
*/
var Footer = React.createClass({
    render: function() {
    //first question, survey not filled out, previous is inactive, submit is inactive
        if(this.props.questionNum == 0 && this.props.responseSize != (this.props.numQuestions)){
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
                    
                    <div className="mdl-cell mdl-cell--2-col"></div>
                    <button className="surveySubmit mdl-cell mdl-cell--8-col mdl-button mdl-js-button mdl-button--raised" disabled>
                        Submit
                    </button>
                    <div className="mdl-cell mdl-cell--2-col"></div>
                </div>
            )
        }
        // first question, survey is filled out, previous is inactive, but we can submit
        else if(this.props.questionNum == 0 && this.props.responseSize == (this.props.numQuestions)){
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
                    
                    <div className="mdl-cell mdl-cell--2-col"></div>
                    <SubmitButton
                    onSubmit={this.props.onSubmit}
                    surveyData={this.props.surveyData}
                    questionID={this.props.questionID}
                    response_format={this.props.response_format}/>
                    <div className="mdl-cell mdl-cell--2-col"></div>
                </div>
            )
        }
        //if we're on the last question for the first time we want to be able to submit but not go to the next question
        else if(this.props.questionNum == (this.props.numQuestions)-1){
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
                    
                    <button className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised" disabled>
                        Next
                    </button>
                    
                    <div className="mdl-cell mdl-cell--2-col"></div>
                    <SubmitButton
                    onSubmit={this.props.onSubmit}
                    surveyData={this.props.surveyData}
                    questionID={this.props.questionID}
                    response_format={this.props.response_format}/>
                    <div className="mdl-cell mdl-cell--2-col"></div>
                </div>
            )
        }
        //if we return to the last question at some point after backtracking it actually requires a different condition since responseSize grows
        else if(this.props.questionNum == (this.props.numQuestions) && this.props.responseSize == this.props.numQuestions){
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
                    
                    <button className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised" disabled>
                        Next
                    </button>
                    
                    <div className="mdl-cell mdl-cell--2-col"></div>
                    <SubmitButton
                    onSubmit={this.props.onSubmit}
                    surveyData={this.props.surveyData}
                    questionID={this.props.questionID}
                    response_format={this.props.response_format}/>
                    <div className="mdl-cell mdl-cell--2-col"></div>
                </div>
            )
        }
        //not the first question, not the last question, and survey not filled out, submit is inactive
    else if(this.props.questionNum != 0 && this.props.questionNum != (this.props.numQuestions) && this.props.responseSize != (this.props.numQuestions)){
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
                
                <div className="mdl-cell mdl-cell--2-col"></div>
                <button className="surveySubmit mdl-cell mdl-cell--8-col mdl-button mdl-js-button mdl-button--raised" disabled>
                    Submit
                </button>
                <div className="mdl-cell mdl-cell--2-col"></div>
            </div>
        )
        }
        //not the first question, not the last question, survey is filled out, all buttons are active
    else if(this.props.questionNum != 0 && this.props.questionNum != (this.props.numQuestions) && this.props.responseSize == (this.props.numQuestions)){
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
                
                <div className="mdl-cell mdl-cell--2-col"></div>
                <SubmitButton
                onSubmit={this.props.onSubmit}
                surveyData={this.props.surveyData}
                questionID={this.props.questionID}
                response_format={this.props.response_format}/>
                <div className="mdl-cell mdl-cell--2-col"></div>

            </div>
        )
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

//creates a progress bar that fills up as you answer questions.
var Progress = React.createClass({
    render: function() {
    var progressValue = (this.props.responseSize/(this.props.numQuestions-1))*100;
        return (
        <progress id="myProgress" className="mdl-cell mdl-cell--4-col bar" value={progressValue} max="100"></progress>
        )
    }
})

//previous button that takes the questionID and the question response data and format and sends it to prevHandler in SurveyDiv
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

//same as previous button but goes to the nextHandler in SurveyDiv
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

//Submit button does the same as the next and previous button but sends to the submitHandler in SurveyDiv
var SubmitButton = React.createClass({
    clickHandler:function(){
        var surveyData = this.props.surveyData;
        var questionID = this.props.questionID;
        var response_format = this.props.response_format;
        this.props.onSubmit(surveyData, questionID, response_format);
    },
    render: function(){
        return(
        <button onClick={this.clickHandler} className="surveySubmit mdl-cell mdl-cell--8-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-color--accent">
                Submit
        </button>
        )
    }
})