/*
* Page is the overall container that gets mounted into our HTML file
*/
var Page = React.createClass({
    //if we're not logged in we want to render a Welcome menu 
    render: function(){
      if (!loggedIn()) {
        return (<Welcome />);
      }
      /*data is a variable defined in dashboard.html as var data = {% raw survey_json %}
      which is a json of the unaswered_surveys list from the db, we map it out so each item
      is a survey that gets it's own SurveyDiv react component'*/
      else{
        routesObject=this.props.routes;
        var itemNodes = data.map(function (item) {
                return (
                <SurveyDiv
                key = {item.id}
                questions={item.questions}
                routes={routesObject}
                surveyID={item.id}
                department={item.department}
                creator={item.creator}
                isInstructor={item.isInstructor}/>
                );
        });
        //return the surveyDiv's in an mdl-grid with a SurveyCreationCard below it (This will probably change after Survey Creation is migrated)
        return (
          <div className="mdl-grid mdl-cell--12-col content">
            <div className="mainDiv">
              {itemNodes}
              <SurveyCreationCard/>
            </div>
          </div>
        );
      }
    }
});

var SurveyDiv = React.createClass({

    /* SurveyDiv contains the overarching json we're looking to submit through ajax as well as a secondary functionality that makes the card disappear after Submit is pressed
    getInitialState initializes our response json in it's state as well as other information we need to know to make everything work */
    getInitialState: function() {
        return({
                length: Object.keys(this.props.questions).length,
                showCard: true,
                iter: 0,
                responseSize: 0,
                response: {
                    survey_id: this.props.surveyID,
                    question_responses:[]
                },
        });
    },
    
    //handler is called in footer.jsx, it receives data about the card that's currently being rendered updating the response state one last time before posting through ajax
    handleSurveySubmit: function(survey,questionID,response_format){
        var response = this.state.response;
        var question_responses_object = {
            response_format: response_format,
            question_id: questionID,
            response_data: survey
        };
        
        //iterate through our question_responses looking to see if the question has previously been answered before, if so we replace the previous answer state by splicing and pushing
        var length = Object.keys(response.question_responses).length;
        for(var i=length-1; i >= 0; i--){
            if(response.question_responses[i].question_id == questionID){
                response.question_responses.splice(i,1);
            }
        }
        response.question_responses.push(question_responses_object);
        this.setState({response: response});

        $.ajax({
            url: this.props.routes.response,
			contentType: 'application/json',
            type: 'POST',
            data: JSON.stringify(response),
            success: function(data){
                console.log(response);
                this.removeCard();
            }.bind(this),
			error: function(xhr, status,err){
                console.log(this.state.response);
				console.error("/api/response", status, err.toString());
			}.bind(this)
        });
    },
    
    //called in the ajax success function, sets showCard to false which will make the SurveyDiv stop rendering 
    removeCard: function() {
        this.setState({showCard: false});
    },
    
    /*nextQuestion and prevQuestion have similar functionality to submit, just without the ajax, we check to see if it's been previously answered
    with a for loop looking to match on questionID and then splicing and pushing if we match (otherwise just pushing) but we also increment or decrement
    this.state.iter*/
    nextQuestion: function(survey,questionID,response_format){
        var response = this.state.response;
        var question_responses_object = {
            response_format: response_format,
            question_id: questionID,
            response_data: survey
        };

        var length = Object.keys(response.question_responses).length;
        for(var i=length-1; i >= 0; i--){
            if(response.question_responses[i].question_id == questionID){
                response.question_responses.splice(i,1);
            }
        }

        response.question_responses.push(question_responses_object);

        this.setState({response: response});
        this.setState({responseSize: Object.keys(this.state.response.question_responses).length});

        var iter = this.state.iter;

        this.setState({iter: iter + 1});
    },

    prevQuestion: function(survey,questionID,response_format){
        var response = this.state.response;
        var question_responses_object = {
            response_format: response_format,
            question_id: questionID,
            response_data: survey
        };

        var length = Object.keys(response.question_responses).length;
        for(var i = length-1; i >= 0; i--){
            if(response.question_responses[i].question_id == questionID){
                response.question_responses.splice(i,1);
            }
        }

        response.question_responses.push(question_responses_object);

        this.setState({response: response});
        this.setState({responseSize: Object.keys(this.state.response.question_responses).length});

        var iter = this.state.iter;


        this.setState({iter: iter - 1});

    },

    render: function() {
        /*if showCard state is true, then we render <Card>, questionID, title, options, response_format vary depending on this.state.iter
        which is manipulated by the previous and next buttons so we can have all the survey's questions on one card.*/
        if(this.state.showCard == true) {
            return(
            <div className="surveyDiv">
                <Card
                routes={this.props.routes}
                questionNum={this.state.iter}
                questionID = {this.props.questions[this.state.iter].id}
                responseSize = {this.state.responseSize}
                numQuestions={this.state.length}
                title={this.props.questions[this.state.iter].title}
                options={this.props.questions[this.state.iter].options}
                response_format={this.props.questions[this.state.iter].response_format}
                surveyID={this.props.surveyID}
                department={this.props.department}
                creator={this.props.creator}
                isInstructor={this.props.isInstructor}
                removeHandler={this.removeCard}
                nextHandler={this.nextQuestion}
                prevHandler={this.prevQuestion}
                onSubmit={this.handleSurveySubmit}
                responseState = {this.state.response.question_responses}/>
            </div>
            );
        }
        else{
        return(
        <div></div>
        );
        }
    }
    });


function loggedIn() {
	return document.cookie.indexOf("user") > -1
}
