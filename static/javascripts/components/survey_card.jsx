/*
* Page with the Card for the creation of surveys
* is passing survey[0].questions
*/

//can pass variables
var SurveysPage = React.createClass({

    /*eventually we'll make some interface to change these states, but
    item_id and item_name should be the same*/
    getInitialState: function(){
        return{
            numQuestion: 0,
            item_id: "testGroup1",
            item_type: "Group",
            item_name: "testGroup1",
            item_title: "",
            questions: [{title: "", response_format: "", options: []}]
        }
    },

    /*update title of survey*/
    updateTitle: function(surveyTitle){
        this.setState({item_title: surveyTitle});
    },


    /*onChange of just about anything, we get an array of json's holding
    each question's data and update our state'*/
    updateQuestions: function(questionObj, questionKey){
        var length = this.state.questions.length;
        var questions = this.state.questions;
        var optionsLength;
        for(var i = length-1; i >= 0; i--){
            if(questionKey == questions[i].key){
                questions[i].title = questionObj.title;
                questions[i].response_format = questionObj.response_format;
                optionsLength = questionObj.options.length;
                questions[i].options = questionObj.options;
            }
        }
        this.setState({questions: questions});
    },

    /*when we click finish survey, we prune the key field off of each question
    json we've made, and then we generate the final Options arrays for each
    option filed in a question, then we post a final json to the api*/

    handleSubmit: function(){
        var questions = this.state.questions;
        var questionsLength = questions.length;
        var optionsLength;
        var finalOptions = [];
        for(var i = questionsLength-1; i >=0; i--){
            delete questions[i].key;
            finalOptions = [];
            optionsLength = questions[i].options.length;
            for(var i2 = optionsLength-1; i2 >= 0; i2--){
                finalOptions.push(questions[i].options[i2].title)
            }
            questions[i].options = finalOptions;
        }
        var surveyObj = {
            item_id : this.state.item_id,
            item_type : this.state.item_type,
            item_name : this.state.item_name,
            item_title: this.state.item_title,
            questions : questions
        };
        console.log(surveyObj);


        $.ajax({
            url: this.props.routes.surveys,
			      contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify(surveyObj),
            success: function(data){
                console.log('Post success');
            }.bind(this),
			error: function(xhr, status,err){
				console.error("/api/response", status, err.toString());
			}.bind(this)
        });
    },

    //mdl in new questions, this probably needs to be moved or repeated
    componentDidUpdate: function(){
        componentHandler.upgradeDom();
    },

    /*this handles adding a new question, we push these nodes
            {
                "title" : "",
                "response_format" : "",
                "options":[],
                "key": null
            }
    to the questions array state, updating the key before pushing*/
    handleAdding: function(newQuestion) {
      var numQuestion= this.state.numQuestion;
      numQuestion = numQuestion + 1;
      newQuestion.key = numQuestion;
      var currQuestions = this.state.questions;
      var newQuestions = currQuestions.push(newQuestion);
      this.setState({
        numQuestion: numQuestion,
        questions: currQuestions
      });
    },

    render: function(){
      return (
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
              <div>
                  <TitleSection titleText="Create a Survey"/>
<div style={{paddingLeft: "30px"}}className="mdl-card__supporting-text mdl-color-text--grey-600">
                  <SurveyTitleCreation titleSurvey={this.state.item_title} updateTitle={this.updateTitle} />
                  <h4>Questions:</h4>
                  </div>
                  <QuestionDiv questions={this.state.questions} updateQuestions={this.updateQuestions} />
                  <AddQuestion onAdding={this.handleAdding}/>
                  <FinishSurvey onSubmit={this.handleSubmit}/>
              </div>
          </div>
      );
    }
});

/*map out a react component for each question we want*/
var QuestionDiv = React.createClass({

render: function(){
    if(this.props.questions.length > 0){
        var questionNodes = this.props.questions.map(function(question) {
          return (
          <Fields questionKey={question.key} updateQuestions={this.props.updateQuestions}/>
          );
        }.bind(this));
    }
    else{
        return(
            <div></div>
        );
    }
  return (
    <div className="commentList">
       {questionNodes}
    </div>
  );
}
});



/*
* Fields controls the overarching data for a question
*/
var Fields = React.createClass({

    //set initial value
    getInitialState: function() {
        return {
            title: '',
            response_format: 'multipleChoice',
            options: [],
        }
    },

    //updates this.state.title
    handleTitleChange: function(event) {
        this.setState({title: event.target.value});
        this.update();
    },

    //updates this.state.response_format
    handleResponseFormatChange: function(event) {
        this.setState({response_format: event.target.value});
        this.update();
    },

    //updates this.state.options
    onOptionsChange: function(options){
        this.setState({options: options});
        this.update();
    },

    //this is called whenever anything updates, sends the question data
    //up to the highest layer real time.
    update: function(){
        var questionObj={
            title: this.state.title,
            response_format: this.state.response_format,
            options: this.state.options
        };
        this.props.updateQuestions(questionObj, this.props.questionKey);
    },

    render: function(){
      return (
          <div className="mdl-card__supporting-text mdl-color-text--grey-600">
                  <div className="mdl-textfield mdl-js-textfield">
                    <input className="mdl-textfield__input"
                    type="text"
                    id="question_title"
                    value={this.state.title}
                    onChange={this.handleTitleChange}/>
                    <label className="mdl-textfield__label">Question title</label>
                  </div>
                  <p>Type:
                     <select
                     id="mySelect"
                     onChange={this.handleResponseFormatChange}
                     value={this.state.value}>
                         <option value="multipleChoice">Multiple Choice</option>
                         <option value="trueOrFalse">Single Choice</option>
                         <option value="rating">Rating Scale</option>
                         <option value="freeResponse">Free Response</option>
                     </select>
                  </p>
                  <OptionsDiv response_format={this.state.response_format} onOptionsChange={this.onOptionsChange}/>
          </div>
      );
    }
});

//depending on this.state.response_format we want to change our options field
//formats
var OptionsDiv = React.createClass({

    render: function(){
        if(this.props.response_format == "multipleChoice"){

          return (
            <div>
            <CheckboxQuestion onOptionsChange={this.props.onOptionsChange}/>
            </div>
          );

        } else if(this.props.response_format == "trueOrFalse"){
          return (
          <div>
          <CheckboxQuestion onOptionsChange={this.props.onOptionsChange}/>
          </div>
          );

        } else if(this.props.response_format == "rating"){
          return (
          <p> Select scale
          </p>
          );

        } else if(this.props.response_format == "freeResponse"){
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



/* controls the data for our options fields*/
var CheckboxQuestion = React.createClass({

    getInitialState: function(){
        return{
            numOptions: 0,
            options: []
        }
    },
    /*called when add option is clicked, pushes a node with a key and blank
    title that we update ourselves, we prune the key in the highest layer
    when we no longer need it for organization*/
    addOption: function(){
        var options = this.state.options;
        var numOptions = this.state.numOptions;
        var optionObject = {
            key: numOptions,
            title: ''
        };
        options.push(optionObject);
        this.setState({
            numOptions: numOptions + 1,
            options: options
        });
    },

    //whenever we change an option we update it's corresponding index in
    //our options array, and also send data up to Fields
    onOptionChange: function(newTitle,key){
        var options=this.state.options;
        var length=options.length;
        for(var i = length-1; i >= 0; i--){
            if(options[i].key==key){
                options[i].title = newTitle;
            }
        }
        this.setState({
            options: options
        });
        this.props.onOptionsChange(options);
    },

    render: function(){
        var renderedOptions = this.state.options.map((option, i) => {
            return(
            <li className="mdl-list__item">
            <CheckboxOption keyProp={option.key} onOptionChange={this.onOptionChange}/>
            </li>
            );
        });

        return (
        <div>
            <ul className="no_bullets mdl-list">
                {renderedOptions}
                <li className="mdl-list__item">
                    <p>
                      <button className="mdl-button mdl-js-button mdl-button--fab mdl-button--mini-fab" onClick={this.addOption}>
                        <i className="material-icons">add</i>
                      </button>
                      &nbsp;&nbsp;&nbsp; ADD OPTION
                    </p>
                </li>
            </ul>
        </div>
      );
    }
});



/*this layer could be merged into MultipleChoiceQuestion fairly easily, renders a text field for every option that we want, onChange it sends data to MultipleChoiceQuestion which starts the chain of it's propagation to the highest layer*/

var CheckboxOption = React.createClass({

    getInitialState: function(){
        return{
            title: ''
        }
    },

    handleChange: function(event){
        this.setState({title: event.target.value});
        this.props.onOptionChange(event.target.value, this.props.keyProp);
    },

    render: function(){
        return(
            <div className="mdl-textfield mdl-js-textfield">
                <p>Enter an option: &nbsp;
                    <input className="mdl-textfield__input"
                    type="text"
                    onChange={this.handleChange}
                    value={this.state.title}/>
                </p>
            </div>
        );
    }
});

/*Called onClick of Add Question button, sends a default JSON to SurveysPage to be added questions state*/
var AddQuestion = React.createClass({
    /*
    * Adding questions
    */
    addQuestion: function() {
       this.props.onAdding(
                {
                "title" : "",
                "response_format" : "",
                "options":[],
                "key": null
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

/*called onClick of Finish Survey button, triggers handleSubmit in SurveysPage
which cleans the data and uses ajax to POST it*/
var FinishSurvey = React.createClass({

    render: function(){
        var style = {
            position: "absolute"
        };
      return (
          <button onClick={this.props.onSubmit} className="mdl-cell mdl-cell--4-col mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent right_button">
              FINISH SURVEY
          </button>
      );
    }
});


var SurveyTitleCreation = React.createClass({
    //set initial value
    getInitialState: function() {
        return {
            item_title: '',
        }
    },

    //updates this.state.title
    handleTitleChange: function(event) {
        this.setState({item_title: event.target.value});
        this.props.updateTitle(event.target.value);
    },

    render: function(){
        return (
            <h4>Survey Title:
                <input className="mdl-textfield__input"
                       type="text"
                       value={this.state.item_title}
                       onChange={this.handleTitleChange}
                /></h4>
        );
    }
});
