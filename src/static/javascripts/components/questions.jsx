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
        var myJsonString = JSON.stringify(this.state.data)
        this.props.onSubmit({myJsonString})
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
        return {data:[]};
    },
    
    handleChange: function(i,value){
        var NewValue = null;
        if(value=="false"){
            NewValue = "true";
        }
        else if(value=="true"){
            NewValue = "false";
        }
        var changeAnswer = this.state.data;
        changeAnswer[i] = NewValue;
        this.setState({data: changeAnswer})
    },
    handleSurveySubmit:function(survey){
        survey.preventDefault();
        var myJsonString = JSON.stringify(this.state.data)
        this.props.onSubmit({myJsonString})
    },
    
    render: function(){
        const renderedOptions = this.props.options.map((option, i) => {
            return (
                <div>
                    <label className="mdl-radio mdl-js-radio mdl-js-ripple-effect">
                      <input type="radio"
                      className="mdl-radio__button"
                      name ={ option }
                      value={ option } 
                      key={ option }
                      onChange={this.handleChange.bind(this,i)}>
                      </input>
                      <span className="mdl-radio__label"> { option } </span>
                    </label>
                </div>
            )
        });

        return (
          <div className="mdl-card__supporting-text mdl-color-text--grey-600">
            <form className="mdl-card__supporting-text mdl-color-text--grey-600">
              { renderedOptions }
              <SubmitButton onSubmit={this.handleSurveySubmit} />
            </form>
          </div>
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
        this.props.onSubmit({answer: answer});
    },
    
  render: function(){
    return (
      <form className="mdl-card__supporting-text mdl-color-text--grey-600">
        <textarea 
        className="mdl-textfield__input"
        type="text"
        rows="4"
        id="test"
        value={this.state.answer}
        onChange={this.handleChange}></textarea>
        <br/>
        <SubmitButton onSubmit={this.handleSurveySubmit}/>
      </form>
     );
  }
});
