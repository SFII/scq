/*
* Page with the Card for the creation of surveys
* is passing survey[0].questions
*/

//can pass variables
var SurveysPage = React.createClass({
    
    getInitialState: function(){
        return{
            numQuestion: 0,
            item_id: "testGroup1",
            item_type: "Group",
            item_name: "testGroup1",
            questions: []
        }
    },
    
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
        console.log(questions);
    },
    
    
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
                console.log(data);
            }.bind(this),
			error: function(xhr, status,err){
				console.error("/api/response", status, err.toString());
			}.bind(this)
        });
    },
    
    onSurveyTitleChange: function(surveyTitle) {
        this.setState({id:surveyTitle});
    },

    //mdl in new questions
    componentDidUpdate: function(){
        componentHandler.upgradeDom();
    },
    
    componentDidMount: function(){
        this.setState({creator_id: user_data[0].id});
        console.log(user_data[0].id);
    },

    handleAdding: function(newQuestion) {
      var numQuestion= this.state.numQuestion;
      numQuestion = numQuestion + 1;
      newQuestion.key = numQuestion;
      var currQuestions = this.state.questions;
      var newQuestions = currQuestions.push(newQuestion);
      this.setState({
        questions: currQuestions
      });
    },

    render: function(){
      return (
          <div className="updates mdl-card mdl-shadow--2dp mdl-cell mdl-cell--4-col mdl-cell--8-col-tablet mdl-cell--12-col-desktop">
              <div>
                  <TitleSection titleText="Create a Survey"/>
                  <div className="mdl-card__supporting-text mdl-color-text--grey-600">
                  <TitleSurvey onSurveyTitleChange={this.onSurveyTitleChange}/>
                  <Creator creator={user_data[0].username}/>
                  <h4>Add Questions:</h4>
                  </div>
                  <QuestionDiv questions={this.state.questions} updateQuestions={this.updateQuestions} />
                  <AddQuestion onAdding={this.handleAdding}/>
                  <FinishSurvey onSubmit={this.handleSubmit}/>
              </div>
          </div>
      );
    }
});

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
* Field is receiving the survey
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
    //set value change
    handleTitleChange: function(event) {
        this.setState({title: event.target.value});
        this.update();
    },
    
    handleResponseFormatChange: function(event) {
        this.setState({response_format: event.target.value});
        this.update();
    },
    
    onOptionsChange: function(options){
        this.setState({options: options});
        this.update();
    },
    
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
                    <label className="mdl-textfield__label">Title of Question:</label>
                  </div>
                  <p>Type:
                     <select 
                     id="mySelect"
                     onChange={this.handleResponseFormatChange}
                     value={this.state.value}>
                         <option disabled value="select"> Select an option </option>
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


var OptionsDiv = React.createClass({
    
    render: function(){
        if(this.props.response_format == "multipleChoice"){

          return (
            <div>
            <MultipleChoiceQuestion onOptionsChange={this.props.onOptionsChange}/>
            </div>
          );

        } else if(this.props.response_format == "trueOrFalse"){
          return (
          <div>
              <SingleChoiceQuestion/>

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




var MultipleChoiceQuestion = React.createClass({
    
    getInitialState: function(){
        return{
            numOptions: 0,
            options: []
        }
    },
    
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
            <MultipleChoiceOption key={option.key} keyProp={option.key} onOptionChange={this.onOptionChange}/>
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

var MultipleChoiceOption = React.createClass({
    
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

var SingleChoiceQuestion = React.createClass({

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


var TitleSurvey = React.createClass({
    /*
    *Input for title
    *
    */
    getInitialState: function(){
        return{
            title: ''
        }
    },
    
    handleChange: function(e){
        this.props.onSurveyTitleChange(e.target.value);
        this.setState({
        title: e.target.value
        });
    },
    
    render: function(){
      return (
          <span>
             <div className="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
             <input className="mdl-textfield__input" 
             value={this.state.title} 
             onChange={this.handleChange}
             type="text" 
             id="item_name"/>
                <label className="mdl-textfield__label">Survey Title</label>
                </div>
          </span>
      );
    }
});

var Creator = React.createClass({
    //TODO: not getting data
    render: function(){
      return (
        <div className="mdl-card__supporting-text mdl-color-text--grey-600">
              <p>Survey creator:&nbsp;{this.props.creator}</p>
        </div>
      );
    }
});
