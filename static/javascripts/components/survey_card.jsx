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

    changeHandler: function() {
        //change handler, modifies the card
        //alert("hello");
    },


    render: function(){
      return (
          <div className="mdl-card__supporting-text mdl-color-text--grey-600">
              <h4>Add a Question:</h4>
              <form>
                  <p>Title:<input type="text" name="title_question"/></p>
                  <p>Type:
                     <select id="select" onChange={this.changeHandler}>
                         <option value="MultipleChoice">Multiple Choice</option>
                         <option value="SingleChoice">Single Choice</option>
                         <option value="Rating">Rating</option>
                         <option value="FreeResponse">Open Response</option>
                     </select>
                  </p>
              </form>

          </div>
      );
    }
});
