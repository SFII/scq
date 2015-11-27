/*
*
*
* Multiple Choice
*/
var MultipleChoice = React.createClass({
    render: function(){
      const renderedOptions = this.props.options.map((option) => {
        return <input type="checkbox" key={ option }>{ option }<br/></input>;
      });

      return (
        <div className="mdl-card__supporting-text mdl-color-text--grey-600">
          <ul className="mdl-card__supporting-text mdl-color-text--grey-600">
            { renderedOptions }
          </ul>
        </div>
      );
    }
});


/*
*
*
* Single Choice
*/
 var SingleChoice = React.createClass({
    render: function(){
        const renderedOptions = this.props.options.map((option, type) => {
          alert(type);
          return <div><input type="radio" name ={ option } value={ option } key={ option }/>{ option }<br/></div>;
        });

        return (
          <div className="mdl-card__supporting-text mdl-color-text--grey-600">
            <form className="mdl-card__supporting-text mdl-color-text--grey-600">
              { renderedOptions }
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
        <p>Insert your text here</p>
        <textarea rows="6" cols="110">
        </textarea>
      </div>
     );
  }
});



