/*
*
* Footer
* Just an mdl submit button, behaves as a normal submit button would
*/
var Footer = React.createClass({
    render: function() {
        return (
        <div className="mdl-card__title mdl-card--expand mdl-300">
        <PrevButton prevHandler={this.props.prevHandler} surveyData={this.props.surveyData}/>
        <NextButton nextHandler={this.props.nextHandler} surveyData={this.props.surveyData}/>
        </div>


        )
    }
})


var Progress = React.createClass({
    render: function() {
        return (
            <div id="p1" class="mdl-progress mdl-js-progress"  style={style1}></div>
        )
    }
})



var PrevButton = React.createClass({
    clickHandler: function() {
        var surveyData = this.props.surveyData;
        this.props.prevHandler(surveyData);
    },
    render: function() {
        return (
        <button onClick={this.clickHandler} className="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
                Previous
            </button>
        )
    }
})

var NextButton = React.createClass({
    clickHandler: function() {
        var surveyData = this.props.surveyData;
        this.props.nextHandler(surveyData);
    },
    render: function() {
        return (
        <button onClick={this.clickHandler} className="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
                &nbsp;&nbsp;&nbsp;Next&nbsp;&nbsp;&nbsp;&nbsp;
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
    //getInitialState finds how many options there are and creates an
    //object questionObj with a corresponding amount of slots set to
    //false and we initialize the data state to be this
    getInitialState: function(){
        var length = Object.keys(this.props.options).length;
        var questionObj =[];
        for(var i =0; i < length; i++){
            questionObj[i]=false;
        }
        return {data: questionObj};
    },
    /*whenever a change happens this is called, the value of the
    checkbox is found, and we go into our data state and set the
    corresponding slot to be the same so the data state matches the
    visual state of the form */

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
    /*once the submit button is clicked we change the data to be a
    JSON object and we send it to the ajax POST*/
    handleSurveySubmit:function(event){

        event.preventDefault();
        var answer = JSON.stringify(this.state.data);
        this.props.onSubmit(answer);
    },
    /*Nothing fancy here, except we also map with an extra parameter i
    which acts as a key value for each option so we can update the state
    correctly*/
    render: function(){
      const renderedOptions = this.props.options.map((option,i) => {
        return (
            <div>
            <label className="mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect">
                <input
                    type="checkbox"
                    key={i}
                    name = {option}
                    value = {this.state.data[i]}
                    className="mdl-checkbox__input"
                    onChange= {this.handleChange.bind(this,i, this.state.data[i])}>
                </input>
                <span className="mdl-checkbox__label"> { option } <br/></span>
            </label>
            </div>
        )
      });
      return (
        <form className="options mdl-cell mdl-cell--4-col mdl-card__supporting-text mdl-color-text--grey-600">
            { renderedOptions }
            <Footer prevHandler={this.props.prevHandler} nextHandler={this.props.nextHandler} surveyData={this.state.data}/>
        </form>
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
    handleSurveySubmit:function(event){

        event.preventDefault();
        var answer = this.state.data;
        console.log(answer);
        this.props.onSubmit({answer});
    },

    render: function(){
        var surveyID = String(this.props.surveyID);
        const renderedOptions = this.props.options.map((option, i) => {
            return (
                <div>
                    <label className="mdl-radio mdl-js-radio mdl-js-ripple-effect">
                    <input type="radio" className="mdl-radio__button" name = {surveyID} value={ option } key={ option }
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
              <Footer prevHandler={this.props.prevHandler} nextHandler={this.props.nextHandler} surveyData={this.state.data}/>
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

    handleSurveySubmit:function(survey){
        survey.preventDefault();
        var answer = this.state.answer.trim();
        this.props.onSubmit(answer);
    },

  render: function(){
    return (
      <form
        className="mdl-card__supporting-text mdl-color-text--grey-600">

        <textarea
        className="mdl-textfield__input"
        type="text"
        rows="4"
        id="test"
        value={this.state.answer}
        onChange={this.handleChange}></textarea>
        <br/>
        <Footer prevHandler={this.props.prevHandler} nextHandler={this.props.nextHandler} surveyData={this.state.answer}/>
      </form>
     );
  }
});
/*
*Rating slider
*This still needs work from Michael and I
*/
var Rating = React.createClass({
   	getInitialState: function(){
		return{data: 5};
	},

	handleChange:function(e){
		this.setState({data: e.target.value});
	},
	 render: function(){
      return (
        <div className="mdl-card__supporting-text mdl-color-text--grey-600">
            <div>
                <input className="mdl-slider mdl-js-slider"
                    type="range"
                    min="0"
                    max="10"
                    value={this.state.data}
                    step="1"
                    onChange={this.handleChange}
                />
                <span id="sliderStatus">{this.state.data}</span>
            </div>
            <Footer />
        </div>
      );
    }
});
