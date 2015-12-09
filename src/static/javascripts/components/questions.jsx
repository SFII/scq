/*
*
* Submit Button
*/
var SubmitButton = React.createClass({
    render: function(){
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
        return {data: [length]};
    },
    
    handleChange: function(){
        this.setState({data[i]: event.target.checked})
    },
    handleSurveySubmit:function(survey){
        survey.preventDefault();
        this.props.onSubmit({survey})
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
                    checked = "checked"
                    className="mdl-checkbox__input" 
                    onchange= {this.handleChange.bind(this,i)}>
                </input>
                <span className="mdl-checkbox__label"> { option } <br/></span>
            </label>
            </div>
        )
      });

      return (
        <form className="mdl-card__supporting-text mdl-color-text--grey-600">
            { renderedOptions }
            <SubmitButton onSubmit={this.handleSurveySubmit}/>
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
    render: function(){
        const renderedOptions = this.props.options.map((option, type) => {
            return (
                <div>
                    <label className="mdl-radio mdl-js-radio mdl-js-ripple-effect">
                      <input type="radio" className="mdl-radio__button" name ={ option } value={ option } key={ option }></input>
                      <span className="mdl-radio__label"> { option } </span>
                    </label>
                </div>
            )
        });

        return (
          <div className="mdl-card__supporting-text mdl-color-text--grey-600">
            <form className="mdl-card__supporting-text mdl-color-text--grey-600">
              { renderedOptions }
              <SubmitButton />
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

  render: function(){
    return (
      <div className="mdl-card__supporting-text mdl-color-text--grey-600">
        <textarea className="mdl-textfield__input" type="text" rows="4" cols="110" id="test"></textarea>
        <br/>
        <SubmitButton />
      </div>
     );
  }
});
