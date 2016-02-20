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
        var responseState = this.props.responseState;
        var responseStateLength = Object.keys(responseState).length;
        var prevAnswers = [];
        for(var i = responseStateLength-1; i >= 0; i--){
          if(responseState[i].question_id == this.props.questionID){
             prevAnswers = responseState[i].response_data;
          }
        }
        return {
            data: questionObj,
            currAnswers: prevAnswers
        };
    },

    handleChange: function(i,value){
        console.log("we in here fam");
        var NewValue = null;
        if(value == false){
            NewValue = true;
        }
        else{
            NewValue = false;
        }
        var changeAnswer = this.state.data;
        changeAnswer[i] = NewValue;
        console.log(this.state.data);
        this.setState({
        data: changeAnswer,
        currAnswers: this.state.data})
    },

    render: function(){
      const renderedOptions = this.props.options.map((option,i) => {
      if(this.state.currAnswers[i] == true){
        return (
            <label className="mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect">
                <input
                    type="checkbox"
                    value = {this.state.data[i]}
                    name = {option}
                    key = {i}
                    className="mdl-checkbox__input"
                    onChange= {this.handleChange.bind(this,i, this.state.data[i])}
                    checked>
                </input>
                <span className="mdl-checkbox__label"> { option } </span>
            </label>
        )
      }
      else{
          return (
                <label className="mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect">
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
      }
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
