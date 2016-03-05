
/*
* Survey. Filled with data to send (JSON)
* survey_handler.py/def _survey_from_request(self):
* models/question.py
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
          "id" : 0,
          "type" : "",
          "question":"",
          "options":[]
      },
  ]
}
];

var finalSurvey = [

  {
  "id": "",
  "item_id":"",
  "item_name":"",
  "item_type":"",
  "creator_name":"",
  "creator_id":"",
  "questions": []
  }
];

var temp = [];

var numQuestion = 0;

/*
* Page with the Card for the creation of surveys
* is passing survey[0].questions
*/

//can pass variables
var SurveyCreationCard = React.createClass({

    loadSurvey: function(){
      this.setState({survey: survey[0].questions});
    },

    componentDidMount: function() {
      this.loadSurvey();
    },

    getInitialState: function() {
      return {survey: []};
    },


    //mdl in new questions
    componentDidUpdate: function(){
        componentHandler.upgradeDom();
    },

    handleAdding: function(newdata) {
      alert("adding");
      numQuestion=numQuestion+1;
      newdata.id = numQuestion;
      var originalsurvey = this.state.survey;
      var temporalsurvey = originalsurvey.concat(newdata);
      this.setState({survey: temporalsurvey});
      temp = temporalsurvey;
      console.log(this.state.survey);
      console.log(temp);
    },

    render: function(){
      return (
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
              <div>
                  <TitleSection titleText="Create a Survey"/>
                  <div className="mdl-card__supporting-text mdl-color-text--grey-600">
                  <TitleSurvey/>
                  <Creator creator={this.props.data}/>
                  <h4>Add Questions:</h4>
                  </div>
                  <FieldDiv survey={this.state.survey} />
                  <AddQuestion onAdding={this.handleAdding}/>
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
        <Fields key={survey.id}/>
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
              <form>
                  <div className="mdl-textfield mdl-js-textfield">
                    <input className="mdl-textfield__input" type="text" id="question_title" onChange={this.Handler}/>
                    <label className="mdl-textfield__label" for="text1">Title of Question:</label>
                  </div>
              </form>

                   <form>
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
    render: function(){

        if(this.props.value == "multipleChoice"){

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
          </p>
          );

        } else if(this.props.value == "freeResponse"){
          return (
          <p> Select maximum of words
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
      <div>
      <form>
          <div className="mdl-textfield mdl-js-textfield">
            <p>Enter an option: &nbsp;<input className="mdl-textfield__input" type="text" id="questin_1" onChange={this.Handler}/></p>
          </div>
      </form>
      <form>
          <div className="mdl-textfield mdl-js-textfield">
            <p>Enter an option: &nbsp;<input className="mdl-textfield__input" type="text" id="questin_1" onChange={this.Handler}/></p>
          </div>
      </form>
      </div>

      );
    }
});






var SQuestions = React.createClass({

    render: function(){
      return (
      <div>
          <form>
              <div className="mdl-textfield mdl-js-textfield">
                <p>Enter an option: &nbsp;<input className="mdl-textfield__input" type="text" id="questin_1" onChange={this.Handler}/></p>
              </div>
          </form>
          <form>
              <div className="mdl-textfield mdl-js-textfield">
                <p>Enter an option: &nbsp;<input className="mdl-textfield__input" type="text" id="questin_1" onChange={this.Handler}/></p>
              </div>
          </form>
      </div>
      );
    }
});


var AddQuestion = React.createClass({
    /*
    * getting initial survey
    */
    getInitialState: function() {
      return {survey: survey};
    },

    /*
    * Adding questions
    */
    addQuestion: function(e) {
       this.props.onAdding(
                {
                "id" : "",
                "type" : "",
                "question":"",
                "options":[]
            });
    },

    render: function(){
      return (
          <button onClick={this.addQuestion} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
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
              FINNISH SURVEY
          </button>
      );
    }
});


var TitleSurvey = React.createClass({
    /*
    *Input for title
    *
    */
    render: function(){
      return (
          <div>
          <form>
             <div className="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                <input className="mdl-textfield__input" type="text" id="item_name"/>
                <label className="mdl-textfield__label" for="text4">Survey Title</label>
             </div>
           </form>
          </div>
      );
    }
});

var Creator = React.createClass({
    //TODO: not getting data
    render: function(){
      return (
        <div className="mdl-card__supporting-text mdl-color-text--grey-600">
              <p>Survey creator:&nbsp;{this.props.username}</p>
        </div>
      );
    }
});
