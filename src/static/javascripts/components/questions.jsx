/*
*
* Submit Button
*/
var SubmitButton = React.createClass({
    render: function() {
        return (
            <button type="submit" className="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect">
                Submit
            </button>
        )
    }
})

/*
*
* Multiple Choice
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
        console.log(value);
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
    handleSurveySubmit:function(event){
        
        event.preventDefault();
        var answer = JSON.stringify(this.state.data);
        this.props.onSubmit({answer});
    },
        
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
        <form 
        className="mdl-card__supporting-text mdl-color-text--grey-600" 
        onSubmit={this.handleSurveySubmit}>
            { renderedOptions }
            <SubmitButton />
        </form>
      );
    }
})
/*
*
*
* Single Choice
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
        console.log(value);
        changeAnswer[i] = true;
        this.setState({data: changeAnswer});
    },
    handleSurveySubmit:function(event){
        
        event.preventDefault();
        var answer = JSON.stringify(this.state.data);
        this.props.onSubmit({answer});
    },
    
    render: function(){
        const renderedOptions = this.props.options.map((option, i) => {
            return (
                <div>
                    <label className="mdl-radio mdl-js-radio mdl-js-ripple-effect">
                    <input type="radio" className="mdl-radio__button" name = "test" value={ option } key={ option }
                     onChange={this.handleChange.bind(this,i,this.state.data[i])}>
                    </input>
                      <span className="mdl-radio__label"> { option } </span>
                    </label>
                </div>    
            )
        });

        return (
            <form 
            className="mdl-card__supporting-text mdl-color-text--grey-600"
            onSubmit={this.handleSurveySubmit}>
            
              { renderedOptions }
              <SubmitButton />
            </form>
        );
    }
});
/*
*
*
* Free
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
        this.props.onSubmit({answer: answer});
    },
    
  render: function(){
    return (
      <form 
        className="mdl-card__supporting-text mdl-color-text--grey-600"
        onSubmit={this.handleSurveySubmit}>
        
        <textarea 
        className="mdl-textfield__input"
        type="text"
        rows="4"
        id="test"
        value={this.state.answer}
        onChange={this.handleChange}></textarea>
        <br/>
        <SubmitButton/>
      </form>
     );
  }
});
/*
*Rating slider
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
            <SubmitButton />
        </div>
      );
    }
});

