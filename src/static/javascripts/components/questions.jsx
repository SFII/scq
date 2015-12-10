/*
*
* Submit Button
*/
var SubmitButton = React.createClass({
    render: function(){
        return (
            <button className="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect">
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
    render: function(){
      const renderedOptions = this.props.options.map((option) => {
        return (
            <div>
            <label className="mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect">
                <input type="checkbox" key={ option } className="mdl-checkbox__input"></input>
                <span className="mdl-checkbox__label"> { option } <br/></span>
            </label>
            </div>
        )
      });

      return (
        <div className="mdl-card__supporting-text mdl-color-text--grey-600">
            { renderedOptions }
            <SubmitButton />
        </div>
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
            const renderedOptions = this.props.options.map((option) => {

		return (
               
                <div>
			<input id="slider1" type="range" min="0" max="10" value={this.state.data} step="1" onChange={this.handleChange}
		 />
			 <span id="sliderStatus">{this.state.data}</span>			

                </div>
            )
});		
      return (
        <div className="mdl-card__supporting-text mdl-color-text--grey-600">
            { renderedOptions }
            <SubmitButton />
        </div>
      );
    }
});

