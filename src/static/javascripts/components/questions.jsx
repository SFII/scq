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
        <button onClick={this.clickHandler} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-color--purple">
                Submit
        </button>
        )
    }
})



/*
*
* Multiple Choice
* All the cards are very similar so I'm not going to copy and paste
*/
var MultipleChoice = React.createClass({
    getInitialState: function(){
        var length = Object.keys(this.props.options).length;
        var questionObj =[];
        for(var i =0; i < length; i++){
            questionObj[i]=false;
        }
        return {data: questionObj};
    },

    handleChange: function(i,value){
        var NewValue = null;
        if(value == false){
            NewValue = true;
        }
        else{
            NewValue = false;
        }
        var changeAnswer = this.state.data;
        changeAnswer[i] = NewValue;
        this.setState({data: changeAnswer})
    },

    render: function(){
      const renderedOptions = this.props.options.map((option,i) => {
        return (
            <label className="mdl-checkbox mdl-js-checkbox">
                <input
                    type="checkbox"
                    value = {this.state.data[i]}
                    name = {option}
                    key = {i}
                    className="mdl-checkbox__input"
                    onChange= {this.handleChange.bind(this,i, this.state.data[i])}>
                </input>
                <span className="mdl-checkbox__label"> { option } </span>
            </label>
        )
      });
      return (
        <div className="options mdl-card__supporting-text mdl-color-text--grey-600">
            { renderedOptions }
            <Footer 
            prevHandler={this.props.prevHandler}
            nextHandler={this.props.nextHandler} 
            onSubmit={this.props.onSubmit}
            surveyData={this.state.data} 
            questionID={this.props.questionID}
            response_format={this.props.response_format}
            questionNum={this.props.questionNum}
            numQuestions={this.props.numQuestions}
            responseSize={this.props.responseSize}/>
        </div>
      );
    }
})
/*
*
*
* Single Choice
* This is the same as multiple choice, but the handlers are different
* so that once a new option is chosen all other options are set to false
* since it simulates a radio form
*/
var SingleChoice = React.createClass({

getInitialState: function(){
        var length = Object.keys(this.props.options).length;
        var questionObj =[];
        for(var i =0; i < length; i++){
            questionObj[i]=false;
        }
        return {data: questionObj};
    },

    handleChange: function(i,value){
        var NewValue = null;
        var length = Object.keys(this.props.options).length;
        var questionObj=[];
        var changeAnswer = this.state.data;
        for(var iter = 0; iter < length; iter++){
            changeAnswer[iter]=false;
        }
        changeAnswer[i] = true;
        this.setState({data: changeAnswer});
    },

    render: function(){
        var surveyID = String(this.props.surveyID);
        const renderedOptions = this.props.options.map((option, i) => {
            return (
                <div>
                    <label className="mdl-radio mdl-js-radio mdl-js-ripple-effect">
                    <input 
                    type="radio" 
                    className="mdl-radio__button"
                    name = {surveyID}
                    value= {i}
                    onChange={this.handleChange.bind(this,i,this.state.data[i])}>
                    </input>
                      <span className="mdl-radio__label"> { option } </span>
                    </label>
                </div>
            )
        });

        return (
            <div
            className="mdl-card__supporting-text mdl-color-text--grey-600">
              { renderedOptions }
              <Footer
              prevHandler={this.props.prevHandler} 
              nextHandler={this.props.nextHandler} 
              onSubmit={this.props.onSubmit}
              surveyData={this.state.data}
              questionID={this.props.questionID}
              response_format={this.props.response_format}
              questionNum={this.props.questionNum}
              numQuestions={this.props.numQuestions}
              responseSize={this.props.responseSize}/>
            </div>
        );
    }
});
/*
*
*
* Free
* Same as the other cards, but simpler, we just take whatever is in the
* textfield and get it to POST
*/
var FreeResponse = React.createClass({

    getInitialState: function(){
        return {answer: 'Change Me'};
    },

    handleChange: function(e){
        this.setState({answer: e.target.value});
    },

  render: function(){
    return (
      <div
        className="mdl-card__supporting-text mdl-color-text--grey-600">

        <textarea
        className="mdl-textfield__input"
        type="text"
        rows="4"
        id="test"
        value={this.state.answer}
        onChange={this.handleChange}></textarea>
        <br/>
        <Footer 
        prevHandler={this.props.prevHandler}
        nextHandler={this.props.nextHandler}
        onSubmit={this.props.onSubmit}
        surveyData={this.state.answer}
        questionID={this.props.questionID}
        response_format={this.props.response_format}
        questionNum={this.props.questionNum}
        numQuestions={this.props.numQuestions}
        responseSize={this.props.responseSize}/>
      </div>
     );
  }
});
/*
*Rating slider
*This still needs work from Michael and I
*/
var Rating = React.createClass({
   	getInitialState: function(){
		return{answer: 5};
	},

	handleChange:function(e){
		this.setState({answer: e.target.value});
	},
	 render: function(){
      return (
        <div className="mdl-card__supporting-text mdl-color-text--grey-600">
            <div>
                <input className="mdl-slider mdl-js-slider"
                    type="range"
                    min="0"
                    max="10"
                    value={this.state.answer}
                    step="1"
                    onChange={this.handleChange}
                />
                <span id="sliderStatus">{this.state.answer}</span>
            </div>
            <Footer 
            prevHandler={this.props.prevHandler}
            nextHandler={this.props.nextHandler}
            onSubmit={this.props.onSubmit}
            surveyData={this.state.answer}
            questionID={this.props.questionID}
            response_format={this.props.response_format}
            questionNum={this.props.questionNum}
            numQuestions={this.props.numQuestions}
            responseSize={this.props.responseSize}/>
            </div>
      );
    }
});
