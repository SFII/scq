
/*
* Survey. Filled with data to send (JSON)
* survey_handler.py/def _survey_from_request(self):
*/
var survey = [

  {
  "id": "",
  "item_id":"",
  "item_name":"",
  "item_type":"",
  "creator_name":"",
  "creator_id":"",
  "questions": [
      {
          "id" : "",
          "type" : "",
          "question":"",
          "options":[]
      }
  ]
}
];


/*
* Page with the Card for the creation of surveys
* is passing survey[0].questions
*/

//can pass variables
var SurveyCreationCard = React.createClass({

    //mdl in new questions
    componentDidUpdate: function(){
        componentHandler.upgradeDom();
    },

    render: function(){
      return (
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
              <div>
                  <TitleSection titleText="Create a Survey"/>
                  <FieldDiv survey={survey[0].questions} />
                  <AddQuestion/>
                  <FinishSurvey/>
              </div>
          </div>
      );
    }
});

var FieldDiv = React.createClass({
render: function(){
    var questionNodes = this.props.survey.map(function(survey) {
      return (
        <Fields/>
      );
    });
  return (
    <div className="commentList">
       {questionNodes}
    </div>
  );
}
});



/*
* Field is receiving the survey
*/
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
              <h4>Add Questions:</h4>
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

    //render different options for multiple & single choice
    /*
    *
    render: function(){

      var mQuestions = [2];
      const options = this.props.options.map((option) => {
        return (
            <p>Hello</p>
        )
      });
    *
    */

    render: function(){

    /*
    *
    type = this.props.value;
    var button = (<div></div>)
    switch (type) {
      case ¨multipleChoice":
        button = <MCQuestion />
    }
    *
    */

        if(this.props.value == "multipleChoice"){
          var mQuestions = [2];


          return (
            <div>
                <MQuestions/>

              <ul className="no_bullets mdl-list">
                <li className="mdl-list__item">
                <p>
                  <button className="mdl-button mdl-js-button mdl-button--fab mdl-button--mini-fab">
                  <i className="material-icons">add</i>

                  </button>

                &nbsp;&nbsp;&nbsp; ADD OPTION
                </p>
               </li>

            </ul>
            </div>
          );

        } else if(this.props.value == "singleChoice"){
          return (
          <div>
              <SQuestions/>

            <ul className="no_bullets mdl-list">
              <li className="mdl-list__item">
              <p>
                <button className="mdl-button mdl-js-button mdl-button--fab mdl-button--mini-fab">
                <i className="material-icons">add</i>

                </button>

              &nbsp;&nbsp;&nbsp; ADD OPTION
              </p>
             </li>

          </ul>
          </div>
          );

        } else if(this.props.value == "rating"){
          return (
          <p> Select scale
          <input type="text" onChange={this.changeHandler}/>
          </p>
          );

        } else if(this.props.value == "freeResponse"){
          return (
          <p> Select maximum of words
          <input type="text" onChange={this.changeHandler}/>
          </p>
          );

        } else {
        return (
        <p onChange={this.changeHandler}></p>
        );
        }
    }
});


var MQuestions = React.createClass({
    render: function(){
      return (
      <ul className="mdl-list">
      <li>
      <input type="text"  onChange={this.changeHandler}/>
      </li>
      <li>
      <input type="text"  onChange={this.changeHandler}/>
      </li>

        </ul>
      );
    }
});


var SQuestions = React.createClass({
    render: function(){
      return (
      <ul className="mdl-list">
      <li>
      <input type="text"  onChange={this.changeHandler}/>
      </li>
      <li>
      <input type="text"  onChange={this.changeHandler}/>
      </li>

        </ul>
      );
    }
});

var AddQuestion = React.createClass({
    clickHandler: function() {
      survey[0].questions.push("option");
    },

    render: function(){
      return (
          <button onClick={this.clickHandler} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
              ADD QUESTION
          </button>
      );
    }
});

var FinishSurvey = React.createClass({

    /* send Survey
    *  url: this.props.routes.surveys, /api/surveys
    *  not finished
    */
    loadPageJSON: function() {
    $.ajax({
    url: '/api/surveys',
    type: 'POST',
    dataType: 'json',
    cache: true,
    success: function(data){
    //on success we set the state of Page to be equal to the JSON received
    this.setState({data: data});
    }.bind(this),
    error: function(xhr, status, err){
    console.error(this.props.routes.surveys, status, err.toString());
    }.bind(this)
    });
    },

    render: function(){
      return (
          <button onClick={this.clickHandler} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent right_button">
              FINISH SURVEY
          </button>
      );
    }
});
