/*
* Page with the Card for the creation of surveys
*/

var SurveyCreationCard = React.createClass({
    render: function(){
      return (
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
              <div>
                  <TitleSection titleText="Create a Survey"/>
                  <Fields/>
              </div>
          </div>
      );
    }
});



var Fields = React.createClass({

    //set initial value
    getInitialState: function() {
        return {value: 'select'};
    },

    //set value change
    changeHandler: function(event) {
        this.setState({value: event.target.value});
    },

    render: function(){
      return (
          <div className="mdl-card__supporting-text mdl-color-text--grey-600">
              <h4>Add a Question:</h4>
              <form>
                  <p>Title:<input type="text" name="title_question"/></p>
                  <p>Type:
                     <select id="mySelect" onChange={this.changeHandler} value={this.state.value}>
                         <option disabled value="select"> Select an option </option>
                         <option value="multipleChoice">Multiple Choice</option>
                         <option value="singleChoice">Single Choice</option>
                         <option value="rating">Rating</option>
                         <option value="freeResponse">Open Response</option>
                     </select>
                  </p>
              </form>
                  <Question value={this.state.value}/>
          </div>
      );
    }
});

var Question = React.createClass({

    changeHandler: function(event) {
        //not sure if needed
        this.setState({value: event.target.value});
    },

    render: function(){

        if(this.props.value == "multipleChoice"){
          return (
          <input type="text" value={this.props.value} onChange={this.changeHandler}/>


        } else if(this.props.value == "singleChoice"){
          return (
            <input type="text" value={this.props.value} onChange={this.changeHandler}/>
          );

        } else if(this.props.value == "rating"){
          return (
            <input type="text" value={this.props.value} onChange={this.changeHandler}/>
          );

        } else if(this.props.value == "freeResponse"){
          return (
            <input type="text" value={this.props.value} onChange={this.changeHandler}/>
          );

        } else {
        return (
        <p onChange={this.changeHandler}></p>
        );
        }
    }
});
